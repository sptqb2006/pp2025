from abc import ABC, abstractmethod


# Abstract Base Class 
class Entity(ABC):
    @abstractmethod
    def input(self):
        """Input entity information"""
        pass

    @abstractmethod
    def list(self):
        """Display entity information"""
        pass


# Student Class
class Student(Entity):
    def __init__(self, sid=None, name=None, dob=None):
        self._id = sid
        self._name = name
        self._dob = dob
    # Getters (encapsulation)
    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def dob(self):
        return self._dob

    # Setters (encapsulation)
    @id.setter
    def id(self, value):
        self._id = value

    @name.setter
    def name(self, value):
        self._name = value

    @dob.setter
    def dob(self, value):
        self._dob = value
    # Polymorphic methods
    def input(self):
        print("\n**** Input student information: id, name, DoB ****")
        self._id = input("Enter student ID: ")
        self._name = input("Enter student name: ")
        self._dob = input("Enter student DoB: ")

    def list(self):
        print(f"ID: {self._id}, Name: {self._name}, DoB: {self._dob}")

    def __str__(self):
        return f"Student(ID: {self._id}, Name: {self._name}, DoB: {self._dob})"

# Course 
class Course(Entity):
    def __init__(self, cid=None, name=None):
        self._id = cid
        self._name = name
    # Getters 
    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name
    # Setters
    @id.setter
    def id(self, value):
        self._id = value

    @name.setter
    def name(self, value):
        self._name = value

    # Polymorphic methods
    def input(self):
        print("\n**** Input Course Information ****")
        self._id = input("Enter Course ID: ")
        self._name = input("Enter Course Name: ")

    def list(self):
        print(f"ID: {self._id}, Name: {self._name}")

    def __str__(self):
        return f"Course(ID: {self._id}, Name: {self._name})"


# Mark Manager Class
class MarkManager:
    def __init__(self):
        self._marks = {}  # {course_id: {student_id: mark}}

    @property
    def marks(self):
        return self._marks

    def input_marks(self, course_id, student_id, mark):
        if course_id not in self._marks:
            self._marks[course_id] = {}
        self._marks[course_id][student_id] = mark

    def get_mark(self, course_id, student_id):
        if course_id in self._marks and student_id in self._marks[course_id]:
            return self._marks[course_id][student_id]
        return None

    def get_course_marks(self, course_id):
        return self._marks.get(course_id, {})


# Collection Manager Class (handles lists of entities with polymorphism)
class EntityCollection:
    def __init__(self):
        self._items = []

    @property
    def items(self):
        return self._items

    def add(self, entity):
        self._items.append(entity)

    def find_by_id(self, entity_id):
        for item in self._items:
            if item.id == entity_id:
                return item
        return None

    def list_all(self, title):
        print(f"\n**** {title} ****")
        for item in self._items:
            item.list()  # Polymorphic call

    def input_multiple(self, entity_class, count):
        for _ in range(count):
            entity = entity_class()
            entity.input()  # Polymorphic call
            self.add(entity)


# Main System Class
class StudentMarkSystem:
    def __init__(self):
        self._students = EntityCollection()
        self._courses = EntityCollection()
        self._mark_manager = MarkManager()

    @property
    def students(self):
        return self._students

    @property
    def courses(self):
        return self._courses

    def setup(self):
        """Initial setup - input students and courses"""
        num_students = int(input("Enter number of students: "))
        self._students.input_multiple(Student, num_students)

        num_courses = int(input("Enter number of courses: "))
        self._courses.input_multiple(Course, num_courses)

    def list_students(self):
        self._students.list_all("Student List")

    def list_courses(self):
        self._courses.list_all("Courses list")

    def input_marks(self):
        print("\n**** Input Marks ****")
        self.list_courses()
        selected_course = input("Select Course ID to input marks: ")

        if self._courses.find_by_id(selected_course) is None:
            print("Course not found!")
            return

        for student in self._students.items:
            mark = float(input(f"Enter mark for student {student.name} (ID: {student.id}): "))
            self._mark_manager.input_marks(selected_course, student.id, mark)

    def show_student_marks(self):
        print("\n--- Show Marks ---")
        self.list_courses()
        selected_course = input("Select Course ID to view marks: ")

        course_marks = self._mark_manager.get_course_marks(selected_course)
        if course_marks:
            print(f"Mark for course: {selected_course}")
            for student in self._students.items:
                mark = self._mark_manager.get_mark(selected_course, student.id)
                if mark is not None:
                    print(f"Student: {student.name} - Mark: {mark}")
                else:
                    print(f"Student: {student.name} - Mark: Not Found")
        else:
            print("No marks found for this course!")

    def run(self):
        """Main menu loop"""
        while True:
            print("\n===========================================================")
            print("USTH STUDENT MARK MANAGEMENT SYSTEM v2.0_OOP by SPTQB_2006")
            print("1. List Students")
            print("2. List Courses")
            print("3. Input Marks for a Course")
            print("4. Show Marks for a Course")
            print("5. Exit")
            choice = input("Enter your choice: ")

            if choice == '1':
                self.list_students()
            elif choice == '2':
                self.list_courses()
            elif choice == '3':
                self.input_marks()
            elif choice == '4':
                self.show_student_marks()
            elif choice == '5':
                break
            else:
                print("Invalid choice!")


# Main
if __name__ == "__main__":
    system = StudentMarkSystem()
    system.setup()
    system.run()
