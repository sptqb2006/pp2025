import tkinter as tk
from tkinter import ttk, messagebox
from .entity import Entity


class Course(Entity):
    def __init__(self, cid=None, name=None, credits=0):
        self._id = cid
        self._name = name
        self._credits = credits

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def credits(self):
        return self._credits

    @id.setter
    def id(self, value):
        self._id = value

    @name.setter
    def name(self, value):
        self._name = value

    @credits.setter
    def credits(self, value):
        self._credits = value

    def input(self):
        print("\n**** Input Course Information ****")
        self._id = input("Enter Course ID: ")
        self._name = input("Enter Course Name: ")
        self._credits = int(input("Enter Course Credits: "))

    def input_gui(self):
        """Input course information via GUI dialog"""
        dialog = tk.Toplevel()
        dialog.title("Input Course Information")
        dialog.geometry("350x200")
        dialog.transient()
        dialog.grab_set()

        result = {'submitted': False}

        ttk.Label(dialog, text="Course ID:").grid(row=0, column=0, padx=10, pady=10, sticky='e')
        id_entry = ttk.Entry(dialog, width=25)
        id_entry.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(dialog, text="Course Name:").grid(row=1, column=0, padx=10, pady=10, sticky='e')
        name_entry = ttk.Entry(dialog, width=25)
        name_entry.grid(row=1, column=1, padx=10, pady=10)

        ttk.Label(dialog, text="Credits:").grid(row=2, column=0, padx=10, pady=10, sticky='e')
        credits_entry = ttk.Entry(dialog, width=25)
        credits_entry.grid(row=2, column=1, padx=10, pady=10)

        def submit():
            try:
                self._id = id_entry.get()
                self._name = name_entry.get()
                self._credits = int(credits_entry.get())
                result['submitted'] = True
                dialog.destroy()
            except ValueError:
                messagebox.showerror("Error", "Credits must be a number!")

        ttk.Button(dialog, text="Submit", command=submit).grid(row=3, column=0, columnspan=2, pady=20)

        dialog.wait_window()
        return result['submitted']

    def list(self):
        print(f"ID: {self._id}, Name: {self._name}, Credits: {self._credits}")

    def __str__(self):
        return f"Course(ID: {self._id}, Name: {self._name}, Credits: {self._credits})"
