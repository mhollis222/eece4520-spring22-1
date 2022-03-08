import tkinter as tk
from tkinter import messagebox
import configparser
settings_path = '../../settings.ini'


class TempWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        # special options to save comments on writes (i hope)
        self.config = configparser.ConfigParser(comment_prefixes='/', allow_no_value=True)
        self.config.read(settings_path)
        self.title("Board Size Window")
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
        self.label1 = tk.Label(self, text='Choose a Board Size (greater than 2)', fg='white',
                               font=("Arial", 35, "bold"), bg='green')
        self.label1.grid(row=0, columnspan=3, sticky=tk.S)

        # enter board size
        self.size_label = tk.Label(self, text='Board Size:', bg='green', font=("Arial", 20), fg='white')
        self.size_label.grid(row=1, column=0, sticky=tk.E, padx=5, pady=5)
        self.size_entry = tk.Entry(self, font=("Arial", 20))
        self.size_entry.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)

        self.save_button = tk.Button(self, text='Save', command=self.save_size,
                                     width=20, height=2, bg='#17850b', fg='white', font=("Arial", 15))
        self.save_button.grid(row=1, column=1, sticky=tk.E, padx=5, pady=5)

    def open_login(self):
        self.destroy()
        self.master.deiconify()  # show the root window

    def save_preferences(self) -> bool:
        """
        Stores the desired settings dict as a yaml file at `settings_path`
        :param settings: the settings to be stored.
        :return: success of operation
        """
        with open(settings_path, 'w') as f:
            self.config.write(f)

    def save_size(self):
        try:
            converted = int(self.size_entry.get())
            if converted % 2 == 0 and converted > 2:
                self.config['Model']['board_height'] = str(converted)
                self.config['Model']['board_width'] = str(converted)
                self.save_preferences()
                messagebox.showerror("", 'Board size successfully updated')
            else:
                messagebox.showerror('Invalid Size', 'Size needs to be an even number and greater than 2')
        except ValueError:
            messagebox.showerror('Invalid Size', 'Must be an integer')

