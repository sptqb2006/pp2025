import tkinter as tk
from tkinter import ttk
from .entity import Entity


class Student(Entity):
    def __init__(self, sid=None, name=None, dob=None):
        self._id = sid
        self._name = name
        self._dob = dob

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def dob(self):
        return self._dob

    @id.setter
    def id(self, value):
        self._id = value

    @name.setter
    def name(self, value):
        self._name = value

    @dob.setter
    def dob(self, value):
        self._dob = value

    def input(self):
        print("\n**** Input student information: id, name, DoB ****")
        self._id = input("Enter student ID: ")
        self._name = input("Enter student name: ")
        self._dob = input("Enter student DoB: ")

    def input_gui(self):
        """Input student information via GUI dialog"""
        dialog = tk.Toplevel()
        dialog.title("Input Student Information")
        dialog.geometry("350x200")
        dialog.transient()
        dialog.grab_set()

        result = {'submitted': False}

        ttk.Label(dialog, text="Student ID:").grid(row=0, column=0, padx=10, pady=10, sticky='e')
        id_entry = ttk.Entry(dialog, width=25)
        id_entry.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(dialog, text="Student Name:").grid(row=1, column=0, padx=10, pady=10, sticky='e')
        name_entry = ttk.Entry(dialog, width=25)
        name_entry.grid(row=1, column=1, padx=10, pady=10)

        ttk.Label(dialog, text="Date of Birth:").grid(row=2, column=0, padx=10, pady=10, sticky='e')
        dob_entry = ttk.Entry(dialog, width=25)
        dob_entry.grid(row=2, column=1, padx=10, pady=10)

        def submit():
            self._id = id_entry.get()
            self._name = name_entry.get()
            self._dob = dob_entry.get()
            result['submitted'] = True
            dialog.destroy()

        ttk.Button(dialog, text="Submit", command=submit).grid(row=3, column=0, columnspan=2, pady=20)

        dialog.wait_window()
        return result['submitted']

    def list(self):
        print(f"ID: {self._id}, Name: {self._name}, DoB: {self._dob}")

    def __str__(self):
        return f"Student(ID: {self._id}, Name: {self._name}, DoB: {self._dob})"
