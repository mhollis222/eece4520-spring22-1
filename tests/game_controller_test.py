import unittest

from mock_ai_player import AIPlayer
from game_controller import *
from human_player import HumanPlayer
from mock_online_player import OnlinePlayer


class MockButton:
    def __init__(self, p1_move: bool):
        if p1_move:
            self.x = 3
            self.y = 5
        else:
            self.x = 2
            self.y = 5


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.game_type = ['local', 'AI', 'online', 'invalid']
        self.p_client = HumanPlayer("client")
        self.player_type = [HumanPlayer("opponent"), AIPlayer("opponent", 3),
                            OnlinePlayer("opponent", game_id=1, human_name="client")]
        self.size = [[4, 4], [8, 8], [12, 12]]

    def human(self):
        return GameController(self.p_client, self.player_type[0], game_id=-1)

    def ai(self):
        return GameController(self.p_client, self.player_type[1], game_id=-1, ai=True)

    def online(self):
        order = [[self.p_client, self.player_type[2]], [self.player_type[2], self.p_client]]
        return GameController(self.p_client, self.player_type[2], game_id=-1, g_order=order[1])

    def make_button(self, order):
        if order == self.p_client:
            return MockButton(p1_move=True)
        else:
            return MockButton(p1_move=False)

    def non_human_flow(self, controller, order, o):
        controller.model.start()
        initial_board = [x[:] for x in controller.model.get_board()]
        if o == order[1]:
            controller.p2.first = True
            controller.advance(None)
            state_a = [x[:] for x in controller.model.get_board()]
            self.assertNotEqual(initial_board, state_a)
            controller.model.active_player = 0
            button = self.make_button(o[1])
            controller.advance(button)
            state_b = [x[:] for x in controller.model.get_board()]
        else:
            controller.p2.first = False
            button = self.make_button(o[0])
            controller.advance(button)
            state_a = [x[:] for x in controller.model.get_board()]
            self.assertNotEqual(initial_board, state_a)
            controller.model.active_player = 1
            controller.advance(None)
            state_b = [x[:] for x in controller.model.get_board()]
        self.assertNotEqual(initial_board, state_b)

    def test_GameFactory(self):
        for gt in self.game_type:
            if gt == 'local':
                p = self.player_type[0]
            elif gt == 'AI':
                p = self.player_type[1]
            elif gt == 'online':
                p = self.player_type[2]
            else:
                p = self.player_type[0]
            order = [[self.p_client, p], [p, self.p_client]]
            for s in self.size:
                for o in order:
                    try:
                        game = GameFactory.get_game(gt, self.p_client, p, s[0], s[1], o)
                        if gt == 'local':
                            self.assertIsInstance(game, Game)
                        elif gt == 'AI':
                            self.assertIsInstance(game, GameDecoratorAI)
                        elif gt == 'online':
                            self.assertIsInstance(game, GameDecoratorOnline)
                        else:
                            self.assertRaises(ValueError)
                    except ValueError:
                        self.assertEqual(gt, 'invalid')

    def test_GameController_init(self):
        controller = None
        for pt in self.player_type:
            if pt.type() == 'Human':
                controller = self.human()
            elif pt.type() == 'AI':
                controller = self.ai()
                self.assertTrue(controller.ai)
            elif pt.type() == 'Online':
                controller = self.online()
                self.assertEqual(controller.game_id, -1)
                self.assertEqual(controller.g_order, [self.player_type[2], self.p_client])
            self.assertIsNotNone(controller)
            self.assertEqual(controller.p1, self.p_client)
            self.assertEqual(controller.p2, pt)

    def test_advance_local(self):
        controller = GameController(self.p_client, self.player_type[0], game_id=-1)
        controller.model = GameFactory.get_game('local', controller.p1, controller.p2,
                                                self.size[1][0], self.size[1][1], controller.g_order)
        controller.model.start()
        initial_board = [x[:] for x in controller.model.get_board()]
        controller.advance(MockButton(p1_move=True))
        state_a = [x[:] for x in controller.model.get_board()]
        self.assertNotEqual(initial_board, state_a)
        controller.advance(MockButton(p1_move=False))
        state_b = controller.model.get_board()
        self.assertNotEqual(state_a, state_b)

    def test_advance_ai(self):
        order = [[self.p_client, self.player_type[1]], [self.player_type[1], self.p_client]]
        for o in order:
            controller = GameController(o[0], o[1], game_id=-1, ai=True, g_order=o)
            controller.model = GameFactory.get_game('AI', controller.p1, controller.p2,
                                                    self.size[1][0], self.size[1][1], controller.g_order)
            self.non_human_flow(controller, order, o)

    def test_advance_online(self):
        order = [[self.p_client, self.player_type[2]], [self.player_type[2], self.p_client]]
        for o in order:
            controller = GameController(o[0], o[1], game_id=-1, g_order=o)
            controller.model = GameFactory.get_game('online', controller.p1, controller.p2,
                                                    self.size[1][0], self.size[1][1], controller.g_order)
            self.non_human_flow(controller, order, o)


if __name__ == '__main__':
    unittest.main()
