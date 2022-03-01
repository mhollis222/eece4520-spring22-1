from tkinter import *
from tkinter import ttk
import tkinter as tk


def main():

    def guest_play():
        new_window = tk.Toplevel()
        new_label = tk.Label(new_window, text='New label')
        new_button = tk.Button(new_window, text='New button')
        new_label.pack()
        new_button.pack()

    def sign_up_page():
        root.destroy()
        register_page = tk.Tk()
        register_page.title("Registration Page")
        register_page.geometry("1000x1000")
        register_page.rowconfigure([0, 1, 2, 3, 4, 5, 6], minsize=50, weight=1)
        register_page.columnconfigure([0, 1], minsize=50, weight=1)
        register_page.configure(bg='green')
        # title
        register_label = tk.Label(text='Sign Up Page', fg='white', font=("Arial", 35, "bold"), bg='green')
        register_label.grid(row=0, columnspan=2, sticky=tk.S)
        # first name
        first_name_label = tk.Label(text='First Name:', bg='green', font=("Arial", 18), fg='white')
        first_name_label.grid(row=1, column=0, sticky=tk.E, padx=5, pady=5)
        first_name_entry = tk.Entry(font=("Arial", 18))
        first_name_entry.grid(row=1, column=1, sticky=tk.W, padx=15, pady=5)
        # last name
        last_name_label = tk.Label(text='Last Name:', bg='green', font=("Arial", 18), fg='white')
        last_name_label.grid(row=2, column=0, sticky=tk.E, padx=5, pady=5)
        last_name_entry = tk.Entry(font=("Arial", 18))
        last_name_entry.grid(row=2, column=1, sticky=tk.W, padx=15, pady=5)
        # username
        new_username_label = tk.Label(text='Username:', bg='green', font=("Arial", 18), fg='white')
        new_username_label.grid(row=3, column=0, sticky=tk.E, padx=5, pady=5)
        new_username_entry = tk.Entry(font=("Arial", 18))
        new_username_entry.grid(row=3, column=1, sticky=tk.W, padx=15, pady=5)
        # password
        new_password_label = tk.Label(text='Password:', bg='green', font=("Arial", 18), fg='white')
        new_password_label.grid(row=4, column=0, sticky=tk.E, padx=5, pady=5)
        new_password_entry = tk.Entry(show='*', font=("Arial", 18))
        new_password_entry.grid(row=4, column=1, sticky=tk.W, padx=15, pady=5)
        # retype password
        retype_password_label = tk.Label(text='Confirm Password:', bg='green', font=("Arial", 18), fg='white')
        retype_password_label.grid(row=5, column=0, sticky=tk.E, padx=5, pady=5)
        retype_password_entry = tk.Entry(show='*', font=("Arial", 18))
        retype_password_entry.grid(row=5, column=1, sticky=tk.W, padx=15, pady=5)
        # login button
        register_button = tk.Button(text='Register', width=20, height=2, font=("Arial", 15))
        register_button.grid(row=6, columnspan=2, padx=5, pady=5, sticky=tk.N)

    # Landing Page for Reversi
    root = tk.Tk()
    root.title("Login Page")
    root.geometry("1000x1000")
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
                              activebackground='green', relief='flat', bd=0, command=sign_up_page)
    register_link.grid(row=4, columnspan=2, sticky=tk.N)
    # OR label
    or_label = tk.Label(text='-OR-', fg='white', font=("Arial", 15, "bold"), bg='green')
    or_label.grid(row=5, columnspan=2, sticky=tk.N)
    # Play as Guest button
    guest_play_button = tk.Button(text='Play as Guest', width=30, height=2, fg='black', font=("Arial", 15),
                                  command=guest_play())
    guest_play_button.grid(row=6, columnspan=2, sticky='n', pady=0)

    root.mainloop()


if __name__ == "__main__":
    main()