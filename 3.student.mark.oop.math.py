import math
import numpy as np
import curses
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


# Course Class - Now with credits
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


# Mark Manager Class -> using numpy array and math.floor
class MarkManager:
    def __init__(self):
        self._marks = {} 

    @property
    def marks(self):
        return self._marks

    def input_marks(self, course_id, student_id, mark):
        # Use math.floor to round down to 1 decimal place
        rounded_mark = math.floor(mark * 10) / 10
        if course_id not in self._marks:
            self._marks[course_id] = {}
        self._marks[course_id][student_id] = rounded_mark

    def get_mark(self, course_id, student_id):
        if course_id in self._marks and student_id in self._marks[course_id]:
            return self._marks[course_id][student_id]
        return None

    def get_course_marks(self, course_id):
        return self._marks.get(course_id, {})

    def get_student_marks_array(self, student_id):
        """Return numpy array of all marks for a student"""
        marks_list = []
        course_ids = []
        for course_id, students in self._marks.items():
            if student_id in students:
                marks_list.append(students[student_id])
                course_ids.append(course_id)
        return np.array(marks_list), course_ids


# Manager Class
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
            item.list()

    def input_multiple(self, entity_class, count):
        for _ in range(count):
            entity = entity_class()
            entity.input()
            self.add(entity)

# Main Class
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
            # Mark is rounded down to 1 decimal using math.floor in MarkManager
            self._mark_manager.input_marks(selected_course, student.id, mark)
        print("Marks have been rounded down to 1 decimal place using math.floor()")

    def show_student_marks(self):
        print("\n--- Show Marks ---")
        self.list_courses()
        selected_course = input("Select Course ID to view marks: ")

        course_marks = self._mark_manager.get_course_marks(selected_course)
        if course_marks:
            print(f"Marks for course: {selected_course}")
            for student in self._students.items:
                mark = self._mark_manager.get_mark(selected_course, student.id)
                if mark is not None:
                    print(f"Student: {student.name} - Mark: {mark}")
                else:
                    print(f"Student: {student.name} - Mark: Not Found")
        else:
            print("No marks found for this course!")

    def calculate_student_gpa(self, student_id):
        """Calculate average GPA for a given student using weighted sum of credits and marks"""
        marks_array, course_ids = self._mark_manager.get_student_marks_array(student_id)

        if len(marks_array) == 0:
            return 0.0

        # Get credits for each course as numpy array
        credits_list = []
        for cid in course_ids:
            course = self._courses.find_by_id(cid)
            if course:
                credits_list.append(course.credits)
            else:
                credits_list.append(0)

        credits_array = np.array(credits_list)

        # Weighted GPA = sum(marks * credits) / sum(credits)
        total_credits = np.sum(credits_array)
        if total_credits == 0:
            return 0.0

        weighted_sum = np.sum(marks_array * credits_array)
        gpa = weighted_sum / total_credits

        return round(gpa, 2)

    def show_student_gpa(self):
        """Show GPA for a specific student"""
        print("\n**** Student GPA ****")
        self.list_students()
        student_id = input("Enter Student ID to calculate GPA: ")

        student = self._students.find_by_id(student_id)
        if student is None:
            print("Student not found!")
            return

        gpa = self.calculate_student_gpa(student_id)
        print(f"\nStudent: {student.name} (ID: {student.id})")
        print(f"Weighted GPA: {gpa}")

    def sort_students_by_gpa(self):
        """Sort student list by GPA descending"""
        print("\n**** Students Sorted by GPA (Descending) ****")

        # Calculate GPA for all students and create list of tuples
        student_gpa_list = []
        for student in self._students.items:
            gpa = self.calculate_student_gpa(student.id)
            student_gpa_list.append((student, gpa))

        # Sort by GPA descending using numpy argsort
        gpas = np.array([item[1] for item in student_gpa_list])
        sorted_indices = np.argsort(-gpas)  # Negative for descending order

        print(f"{'Rank':<6}{'ID':<12}{'Name':<20}{'GPA':<10}")
        print("-" * 48)
        for rank, idx in enumerate(sorted_indices, 1):
            student, gpa = student_gpa_list[idx]
            print(f"{rank:<6}{student.id:<12}{student.name:<20}{gpa:<10}")

    def run(self):
        """Main menu loop"""
        while True:
            print("\n" + "=" * 60)
            print("  USTH STUDENT MARK MANAGEMENT SYSTEM v3.0")
            print("=" * 60)
            print("1. List Students")
            print("2. List Courses")
            print("3. Input Marks for a Course")
            print("4. Show Marks for a Course")
            print("5. Show Student GPA")
            print("6. Sort Students by GPA (Descending)")
            print("7. Exit")
            print("-" * 60)
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
                self.show_student_gpa()
            elif choice == '6':
                self.sort_students_by_gpa()
            elif choice == '7':
                print("Goodbye!")
                break
            else:
                print("Invalid choice!")

# Curses UI Version
def curses_main(stdscr):
    """Curses-decorated UI"""
    curses.curs_set(1)
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)

    system = StudentMarkSystem()

    def safe_addstr(stdscr, row, col, text, attr=0):
        """Safely add string, checking screen bounds"""
        max_y, max_x = stdscr.getmaxyx()
        if row < max_y and col < max_x:
            stdscr.addstr(row, col, text[:max_x - col - 1], attr)

    def draw_header(stdscr):
        attr = curses.color_pair(1) | curses.A_BOLD
        safe_addstr(stdscr, 0, 0, "=" * 60, attr)
        safe_addstr(stdscr, 1, 0, "  USTH STUDENT MARK MANAGEMENT SYSTEM v3.0", attr)
        safe_addstr(stdscr, 2, 0, "  OOP + Math + NumPy + Curses by SPTQB_2006", attr)
        safe_addstr(stdscr, 3, 0, "=" * 60, attr)

    def draw_menu(stdscr):
        attr = curses.color_pair(2)
        menu_items = [
            "1. List Students",
            "2. List Courses",
            "3. Input Marks for a Course",
            "4. Show Marks for a Course",
            "5. Show Student GPA",
            "6. Sort Students by GPA (Descending)",
            "7. Exit"
        ]
        for i, item in enumerate(menu_items):
            safe_addstr(stdscr, 5 + i, 2, item, attr)

    def get_input(stdscr, prompt, row):
        safe_addstr(stdscr, row, 2, prompt)
        curses.echo()
        inp = stdscr.getstr(row, len(prompt) + 3, 50).decode('utf-8')
        curses.noecho()
        return inp

    while True:
        stdscr.clear()
        max_y, max_x = stdscr.getmaxyx()
        draw_header(stdscr)
        draw_menu(stdscr)

        safe_addstr(stdscr, 13, 2, "Enter choice: ", curses.color_pair(3))
        stdscr.refresh()

        curses.echo()
        choice = stdscr.getstr(13, 16, 2).decode('utf-8')
        curses.noecho()

        if choice == '7':
            break

        stdscr.clear()
        draw_header(stdscr)

        if choice == '6':
            safe_addstr(stdscr, 5, 2, "Students Sorted by GPA (Descending):")
            safe_addstr(stdscr, 6, 2, "-" * 50)
            row = 7
            student_gpa_list = []
            for student in system._students.items:
                gpa = system.calculate_student_gpa(student.id)
                student_gpa_list.append((student, gpa))

            if student_gpa_list:
                gpas = np.array([item[1] for item in student_gpa_list])
                sorted_indices = np.argsort(-gpas)
                for rank, idx in enumerate(sorted_indices, 1):
                    student, gpa = student_gpa_list[idx]
                    safe_addstr(stdscr, row, 2, f"{rank}. {student.name} (ID: {student.id}) - GPA: {gpa}")
                    row += 1
                    if row >= max_y - 2:
                        break
            else:
                safe_addstr(stdscr, row, 2, "No students found.")

        # Show prompt at bottom of screen
        prompt_row = min(max_y - 2, 18)
        safe_addstr(stdscr, prompt_row, 2, "Press any key to continue...")
        stdscr.refresh()
        stdscr.getch()


# Main
if __name__ == "__main__":
    print("Select mode:")
    print("1. Standard Console Mode")
    print("2. Curses UI Mode")
    mode = input("Enter choice (1/2): ")

    if mode == '2':
        curses.wrapper(curses_main)
    else:
        system = StudentMarkSystem()
        system.setup()
        system.run()
