import tkinter as tk


class ReversiButton(tk.Button):
    def __init__(self, x: int, y: int, text, callback, state, color, **kwargs):
        super(ReversiButton, self).__init__(**kwargs)
        self.x = x
        self.y = y
        # 0 = empty, 1 = p1, 2 = p2, 3 = potential move
        self['state'] = state
        self.text = text
        self['text'] = self.text
        self['bg'] = color
        self.command = lambda: callback(self)
        self['command'] = self.command

    def change_state(self, event,  state: int):
        self.state = state
        self['text'] = str(state)


def action(x: int, y: int, button: ReversiButton):
    print(str(x) + str(y))
