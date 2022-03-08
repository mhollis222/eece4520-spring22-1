from tkinter import *
import tkinter as tk


class AlignmentWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Settings Window")
        self.geometry("2000x2000")
        self.rowconfigure([0, 1, 2], minsize=50, weight=1)
        self.columnconfigure([0, 1, 2], minsize=50, weight=1)
        self.configure(bg='green')

        # back button
        self.back_button = tk.Button(self, text='Back', width=10, height=2, font=("Arial", 12),
                                     activebackground='green', bg='green', fg='white', relief='flat',
                                     command=self.open_login)
        self.back_button.grid(row=0, column=0, padx=0, sticky='nw')

        # title
        self.label1 = tk.Label(self, text='Board Alignment', fg='white',
                               font=("Arial", 35, "bold"), bg='green')
        self.label1.grid(row=0, columnspan=3, sticky=tk.S)

        # checkbox

        #def isChecked():
        #   if start_filled.get() == 1:
        #       btn['state'] = NORMAL
        #       btn.configure(text='on!')
        #   elif start_filled.get() == 0:
        #       btn['state'] = DISABLED
        #       btn.configure(text='off!')

        start_filled = IntVar()  # means checkbox is checked
        tk.Checkbutton(self, text='Start at Center', bg='green', font=("Arial", 20), fg='white',
                       variable=start_filled, onvalue=1, offvalue=0,
                       ).grid(row=1, column=1, sticky=tk.W)

        #btn = Button(self, state=DISABLED, padx=20, pady=5)
        #btn.pack()

    def open_login(self):
        self.destroy()
        self.master.deiconify()  # show the root window
