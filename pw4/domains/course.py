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

    def list(self):
        print(f"ID: {self._id}, Name: {self._name}, Credits: {self._credits}")

    def __str__(self):
        return f"Course(ID: {self._id}, Name: {self._name}, Credits: {self._credits})"
