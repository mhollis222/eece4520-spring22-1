import tkinter as tk
from PIL import Image, ImageTk

class ReversiButton(tk.Button):
    def __init__(self, root,  x: int, y: int, text, callback, state, color, **kwargs):
        super(ReversiButton, self).__init__(root)
        self.x = x
        self.y = y
        # 0 = empty, 1 = p1, 2 = p2, 3 = potential move
        self['state'] = state
        self.text = text
        self['text'] = self.text

        # if color == 'black':
        #     self.icon = Image.open('../View/UI/images/black_chip.png')
        # elif color == 'white':
        #     self.icon = Image.open('../View/UI/images/white_chip.png')
        # elif color == 'blue':
        #     self.icon = Image.open('../View/UI/images/blue_chip.png')
        # elif color == 'pink':
        #     self.icon = Image.open('../View/UI/images/pink_chip.png')
        # elif color == 'cyan':
        #     self.icon = Image.open('../View/UI/images/cyan_chip.png')
        # else:
        #     self.icon = Image.open('../View/UI/images/red_chip.png')
        #
        # self.icon = self.icon.resize((150, 150))
        # self.icon = ImageTk.PhotoImage(self.icon)
        # self['image'] = ImageTk.PhotoImage(self.icon)

        self['bg'] = color
        self['activebackground'] = color
        self.command = lambda: callback(self)
        self['command'] = self.command

    def change_state(self, event,  state: int):
        '''
        Helper function used to change the state of buttons to either disabled or active
        :param state: int
        :return:
        '''
        self.state = state
        self['text'] = str(state)


def action(x: int, y: int, button: ReversiButton):
    print(str(x) + str(y))
