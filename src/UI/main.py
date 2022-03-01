from tkinter import *
from tkinter import ttk
import tkinter as tk


def main():
    root = tk.Tk()
    root.title("Login Page")
    root.geometry("800x800")
    root.rowconfigure([0, 1, 2, 3, 4, 5, 6], minsize=50, weight=1)
    root.columnconfigure([0, 1], minsize=50, weight=1)
    root.configure(bg='green')

    # title
    label1 = tk.Label(text='Reversi', fg='white', font=("Arial", 55, "bold"), bg='green')
    label1.grid(row=0, columnspan=2, sticky=tk.S)
    # username
    username_label = tk.Label(text='Username:', bg='green', font=("Arial", 20), fg='white')
    username_label.grid(row=1, column=0, sticky=tk.E, padx=5, pady=5)
    username_entry = tk.Entry(font=("Arial", 20))
    username_entry.grid(row=1, column=1, sticky=tk.W, padx=15, pady=5)
    # password
    password_label = tk.Label(text='Password:', bg='green', font=("Arial", 20), fg='white')
    password_label.grid(row=2, column=0, sticky=tk.E, padx=5, pady=5)
    password_entry = tk.Entry(show='*', font=("Arial", 20))
    password_entry.grid(row=2, column=1, sticky=tk.W, padx=15, pady=5)
    # login button
    login_button = tk.Button(text='Login', width=30, height=2, font=("Arial", 15))
    login_button.grid(row=3, columnspan=2, padx=5, pady=5)
    # register link
    register_link = tk.Button(text='Not a member? Sign Up', fg='white', font=("Arial", 15), bg='green',
                              activebackground='green', relief='flat', bd=0)
    register_link.grid(row=4, columnspan=2, sticky=tk.N)
    # OR label
    or_label = tk.Label(text='-OR-', fg='white', font=("Arial", 15, "bold"), bg='green')
    or_label.grid(row=5, columnspan=2, sticky=tk.N)
    # Play as Guest button
    guest_play_button = tk.Button(text='Play as Guest', width=30, height=2, fg='black', font=("Arial", 15))
    guest_play_button.grid(row=6, columnspan=2, sticky='n', pady=0)

    root.mainloop()


if __name__ == "__main__":
    main()