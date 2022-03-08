# import tkinter as tk
# from login_window import LoginWindow
#
#
# class App(tk.Tk):
#     def __init__(self):
#         super().__init__()
#
#         self.title('Main window')
#         self.geometry('1000x1000')
#
#         self.login_button = tk.Button(self, text='Login', command=self.open_login)
#         self.login_button.pack()
#         self.register_button = tk.Button(self, text='Register')
#         self.register_button.pack()
#         self.close_button = tk.Button(self, text='Close', command=self.destroy)
#         self.close_button.pack()
#
#     def open_login(self):
#         login_win = LoginWindow(self)
#         login_win.focus_force()
#         self.withdraw()
