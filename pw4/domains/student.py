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

    def list(self):
        print(f"ID: {self._id}, Name: {self._name}, DoB: {self._dob}")

    def __str__(self):
        return f"Student(ID: {self._id}, Name: {self._name}, DoB: {self._dob})"
