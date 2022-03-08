import tkinter as tk


class TempWindow(tk.Toplevel):
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
        self.label1 = tk.Label(self, text='Choose a Board Size (greater than 4)', fg='white',
                               font=("Arial", 35, "bold"), bg='green')
        self.label1.grid(row=0, columnspan=3, sticky=tk.S)

        # enter board size
        self.size_label = tk.Label(self, text='Board Size:', bg='green', font=("Arial", 20), fg='white')
        self.size_label.grid(row=1, column=0, sticky=tk.E, padx=5, pady=5)
        self.size_entry = tk.Entry(self, font=("Arial", 20))
        self.size_entry.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)

    def open_login(self):
        self.destroy()
        self.master.deiconify()  # show the root window
