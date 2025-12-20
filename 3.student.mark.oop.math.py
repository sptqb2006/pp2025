import math
import numpy as np
import curses
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
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

    def input_multiple_gui(self, entity_class, count):
        """Input multiple entities via GUI"""
        for _ in range(count):
            entity = entity_class()
            if entity.input_gui():
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

    def setup_gui(self, root):
        """Initial setup via GUI - input students and courses"""
        num_students = simpledialog.askinteger("Setup", "Enter number of students:", parent=root, minvalue=1)
        if num_students:
            self._students.input_multiple_gui(Student, num_students)

        num_courses = simpledialog.askinteger("Setup", "Enter number of courses:", parent=root, minvalue=1)
        if num_courses:
            self._courses.input_multiple_gui(Course, num_courses)

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

    def input_marks_gui(self, root):
        """Input marks via GUI dialog"""
        if not self._courses.items:
            messagebox.showwarning("Warning", "No courses available!")
            return

        # Select course dialog
        dialog = tk.Toplevel(root)
        dialog.title("Input Marks")
        dialog.geometry("400x350")
        dialog.transient(root)
        dialog.grab_set()

        ttk.Label(dialog, text="Select Course:").pack(pady=10)

        course_var = tk.StringVar()
        course_combo = ttk.Combobox(dialog, textvariable=course_var, state="readonly", width=30)
        course_combo['values'] = [f"{c.id} - {c.name}" for c in self._courses.items]
        if course_combo['values']:
            course_combo.current(0)
        course_combo.pack(pady=5)

        ttk.Label(dialog, text="Enter Marks for Students:").pack(pady=10)

        # Frame for student marks
        marks_frame = ttk.Frame(dialog)
        marks_frame.pack(fill='both', expand=True, padx=10)

        mark_entries = {}
        for i, student in enumerate(self._students.items):
            ttk.Label(marks_frame, text=f"{student.name} ({student.id}):").grid(row=i, column=0, padx=5, pady=3, sticky='e')
            entry = ttk.Entry(marks_frame, width=10)
            entry.grid(row=i, column=1, padx=5, pady=3)
            mark_entries[student.id] = entry

        def submit():
            course_selection = course_var.get()
            if not course_selection:
                messagebox.showerror("Error", "Please select a course!")
                return
            course_id = course_selection.split(" - ")[0]

            for student_id, entry in mark_entries.items():
                try:
                    mark = float(entry.get())
                    self._mark_manager.input_marks(course_id, student_id, mark)
                except ValueError:
                    messagebox.showerror("Error", f"Invalid mark for student {student_id}!")
                    return

            messagebox.showinfo("Success", "Marks saved (rounded down to 1 decimal)")
            dialog.destroy()

        ttk.Button(dialog, text="Submit", command=submit).pack(pady=15)
        dialog.wait_window()

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
    """Curses-decorated UI with full input support"""
    curses.curs_set(1)
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)

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
            "0. Setup (Input Students & Courses)",
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
        """Get string input from user"""
        safe_addstr(stdscr, row, 2, prompt)
        stdscr.refresh()
        curses.echo()
        inp = stdscr.getstr(row, len(prompt) + 3, 50).decode('utf-8')
        curses.noecho()
        return inp

    def get_int_input(stdscr, prompt, row):
        """Get integer input from user"""
        while True:
            try:
                val = get_input(stdscr, prompt, row)
                return int(val)
            except ValueError:
                safe_addstr(stdscr, row + 1, 2, "Invalid number! Try again.", curses.color_pair(4))
                stdscr.refresh()

    def get_float_input(stdscr, prompt, row):
        """Get float input from user"""
        while True:
            try:
                val = get_input(stdscr, prompt, row)
                return float(val)
            except ValueError:
                safe_addstr(stdscr, row + 1, 2, "Invalid number! Try again.", curses.color_pair(4))
                stdscr.refresh()

    def wait_for_key(stdscr, row):
        """Wait for user to press any key"""
        safe_addstr(stdscr, row, 2, "Press any key to continue...")
        stdscr.refresh()
        stdscr.getch()

    def input_students_curses(stdscr):
        """Input students using curses"""
        stdscr.clear()
        draw_header(stdscr)
        safe_addstr(stdscr, 5, 2, "**** Input Students ****", curses.color_pair(1))

        num = get_int_input(stdscr, "Enter number of students: ", 7)

        for i in range(num):
            stdscr.clear()
            draw_header(stdscr)
            safe_addstr(stdscr, 5, 2, f"**** Student {i+1}/{num} ****", curses.color_pair(1))

            sid = get_input(stdscr, "Student ID: ", 7)
            name = get_input(stdscr, "Student Name: ", 8)
            dob = get_input(stdscr, "Date of Birth: ", 9)

            student = Student(sid, name, dob)
            system._students.add(student)

            safe_addstr(stdscr, 11, 2, f"Student '{name}' added!", curses.color_pair(3))
            wait_for_key(stdscr, 13)

    def input_courses_curses(stdscr):
        """Input courses using curses"""
        stdscr.clear()
        draw_header(stdscr)
        safe_addstr(stdscr, 5, 2, "**** Input Courses ****", curses.color_pair(1))

        num = get_int_input(stdscr, "Enter number of courses: ", 7)

        for i in range(num):
            stdscr.clear()
            draw_header(stdscr)
            safe_addstr(stdscr, 5, 2, f"**** Course {i+1}/{num} ****", curses.color_pair(1))

            cid = get_input(stdscr, "Course ID: ", 7)
            name = get_input(stdscr, "Course Name: ", 8)
            credits = get_int_input(stdscr, "Credits: ", 9)

            course = Course(cid, name, credits)
            system._courses.add(course)

            safe_addstr(stdscr, 11, 2, f"Course '{name}' added!", curses.color_pair(3))
            wait_for_key(stdscr, 13)

    def list_students_curses(stdscr):
        """List all students"""
        stdscr.clear()
        draw_header(stdscr)
        max_y, _ = stdscr.getmaxyx()
        safe_addstr(stdscr, 5, 2, "**** Student List ****", curses.color_pair(1))
        safe_addstr(stdscr, 6, 2, "-" * 50)

        if not system._students.items:
            safe_addstr(stdscr, 7, 2, "No students found.")
        else:
            row = 7
            for s in system._students.items:
                if row >= max_y - 2:
                    break
                safe_addstr(stdscr, row, 2, f"ID: {s.id}, Name: {s.name}, DoB: {s.dob}")
                row += 1

        wait_for_key(stdscr, min(row + 1, max_y - 2))

    def list_courses_curses(stdscr):
        """List all courses"""
        stdscr.clear()
        draw_header(stdscr)
        max_y, _ = stdscr.getmaxyx()
        safe_addstr(stdscr, 5, 2, "**** Course List ****", curses.color_pair(1))
        safe_addstr(stdscr, 6, 2, "-" * 50)

        if not system._courses.items:
            safe_addstr(stdscr, 7, 2, "No courses found.")
        else:
            row = 7
            for c in system._courses.items:
                if row >= max_y - 2:
                    break
                safe_addstr(stdscr, row, 2, f"ID: {c.id}, Name: {c.name}, Credits: {c.credits}")
                row += 1

        wait_for_key(stdscr, min(row + 1, max_y - 2))

    def input_marks_curses(stdscr):
        """Input marks for a course"""
        stdscr.clear()
        draw_header(stdscr)
        max_y, _ = stdscr.getmaxyx()
        safe_addstr(stdscr, 5, 2, "**** Input Marks ****", curses.color_pair(1))

        if not system._courses.items:
            safe_addstr(stdscr, 7, 2, "No courses available!", curses.color_pair(4))
            wait_for_key(stdscr, 9)
            return

        if not system._students.items:
            safe_addstr(stdscr, 7, 2, "No students available!", curses.color_pair(4))
            wait_for_key(stdscr, 9)
            return

        # Show courses
        safe_addstr(stdscr, 7, 2, "Available Courses:")
        row = 8
        for c in system._courses.items:
            if row >= max_y - 6:
                break
            safe_addstr(stdscr, row, 4, f"{c.id} - {c.name}")
            row += 1

        course_id = get_input(stdscr, "Enter Course ID: ", row + 1)

        if system._courses.find_by_id(course_id) is None:
            safe_addstr(stdscr, row + 3, 2, "Course not found!", curses.color_pair(4))
            wait_for_key(stdscr, row + 5)
            return

        # Input marks for each student
        for student in system._students.items:
            while True:
                stdscr.clear()
                draw_header(stdscr)
                safe_addstr(stdscr, 5, 2, f"Course: {course_id}", curses.color_pair(1))
                safe_addstr(stdscr, 6, 2, f"Student: {student.name} (ID: {student.id})")

                mark = get_float_input(stdscr, "Enter mark (0-20): ", 8)
                if mark < 0 or mark > 20:
                    safe_addstr(stdscr, 10, 2, "Error: Mark must be between 0 and 20!", curses.color_pair(4))
                    safe_addstr(stdscr, 11, 2, "Press any key to try again...")
                    stdscr.refresh()
                    stdscr.getch()
                    continue
                break
            system._mark_manager.input_marks(course_id, student.id, mark)

            safe_addstr(stdscr, 10, 2, "Mark saved!", curses.color_pair(3))
            stdscr.refresh()
            curses.napms(500)  # Brief pause

        stdscr.clear()
        draw_header(stdscr)
        safe_addstr(stdscr, 5, 2, "All marks saved! (Rounded down to 1 decimal)", curses.color_pair(3))
        wait_for_key(stdscr, 7)

    def show_marks_curses(stdscr):
        """Show marks for a course"""
        stdscr.clear()
        draw_header(stdscr)
        max_y, _ = stdscr.getmaxyx()
        safe_addstr(stdscr, 5, 2, "**** Show Marks ****", curses.color_pair(1))

        if not system._courses.items:
            safe_addstr(stdscr, 7, 2, "No courses available!", curses.color_pair(4))
            wait_for_key(stdscr, 9)
            return

        # Show courses
        safe_addstr(stdscr, 7, 2, "Available Courses:")
        row = 8
        for c in system._courses.items:
            if row >= max_y - 6:
                break
            safe_addstr(stdscr, row, 4, f"{c.id} - {c.name}")
            row += 1

        course_id = get_input(stdscr, "Enter Course ID: ", row + 1)

        stdscr.clear()
        draw_header(stdscr)
        safe_addstr(stdscr, 5, 2, f"Marks for Course: {course_id}", curses.color_pair(1))
        safe_addstr(stdscr, 6, 2, "-" * 50)

        course_marks = system._mark_manager.get_course_marks(course_id)
        row = 7
        if course_marks:
            for student in system._students.items:
                if row >= max_y - 2:
                    break
                mark = system._mark_manager.get_mark(course_id, student.id)
                if mark is not None:
                    safe_addstr(stdscr, row, 2, f"{student.name}: {mark}")
                else:
                    safe_addstr(stdscr, row, 2, f"{student.name}: Not Found")
                row += 1
        else:
            safe_addstr(stdscr, row, 2, "No marks found for this course!")

        wait_for_key(stdscr, min(row + 1, max_y - 2))

    def show_gpa_curses(stdscr):
        """Show GPA for a student"""
        stdscr.clear()
        draw_header(stdscr)
        max_y, _ = stdscr.getmaxyx()
        safe_addstr(stdscr, 5, 2, "**** Student GPA ****", curses.color_pair(1))

        if not system._students.items:
            safe_addstr(stdscr, 7, 2, "No students available!", curses.color_pair(4))
            wait_for_key(stdscr, 9)
            return

        # Show students
        safe_addstr(stdscr, 7, 2, "Available Students:")
        row = 8
        for s in system._students.items:
            if row >= max_y - 6:
                break
            safe_addstr(stdscr, row, 4, f"{s.id} - {s.name}")
            row += 1

        student_id = get_input(stdscr, "Enter Student ID: ", row + 1)

        student = system._students.find_by_id(student_id)
        if student is None:
            safe_addstr(stdscr, row + 3, 2, "Student not found!", curses.color_pair(4))
            wait_for_key(stdscr, row + 5)
            return

        gpa = system.calculate_student_gpa(student_id)

        stdscr.clear()
        draw_header(stdscr)
        safe_addstr(stdscr, 5, 2, f"Student: {student.name} (ID: {student.id})", curses.color_pair(1))
        safe_addstr(stdscr, 7, 2, f"Weighted GPA: {gpa}", curses.color_pair(3))
        wait_for_key(stdscr, 9)

    def sort_by_gpa_curses(stdscr):
        """Sort and display students by GPA"""
        stdscr.clear()
        draw_header(stdscr)
        max_y, _ = stdscr.getmaxyx()
        safe_addstr(stdscr, 5, 2, "Students Sorted by GPA (Descending):", curses.color_pair(1))
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

        wait_for_key(stdscr, min(row + 1, max_y - 2))

    # Main loop
    while True:
        stdscr.clear()
        max_y, max_x = stdscr.getmaxyx()
        draw_header(stdscr)
        draw_menu(stdscr)

        safe_addstr(stdscr, 14, 2, "Enter choice: ", curses.color_pair(3))
        stdscr.refresh()

        curses.echo()
        choice = stdscr.getstr(14, 16, 2).decode('utf-8')
        curses.noecho()

        if choice == '7':
            break
        elif choice == '0':
            input_students_curses(stdscr)
            input_courses_curses(stdscr)
        elif choice == '1':
            list_students_curses(stdscr)
        elif choice == '2':
            list_courses_curses(stdscr)
        elif choice == '3':
            input_marks_curses(stdscr)
        elif choice == '4':
            show_marks_curses(stdscr)
        elif choice == '5':
            show_gpa_curses(stdscr)
        elif choice == '6':
            sort_by_gpa_curses(stdscr)
        else:
            stdscr.clear()
            draw_header(stdscr)
            safe_addstr(stdscr, 5, 2, "Invalid choice!", curses.color_pair(4))
            wait_for_key(stdscr, 7)


# Tkinter GUI Main
def tkinter_main():
    """Tkinter GUI main"""
    root = tk.Tk()
    root.title("USTH Student Mark Management System v3.0")
    root.geometry("500x450")

    system = StudentMarkSystem()

    # Header
    header_frame = ttk.Frame(root)
    header_frame.pack(fill='x', padx=10, pady=10)
    ttk.Label(header_frame, text="USTH STUDENT MARK MANAGEMENT SYSTEM v3.0",
              font=('Helvetica', 14, 'bold')).pack()

    # Output Text Area
    output_frame = ttk.Frame(root)
    output_frame.pack(fill='both', expand=True, padx=10, pady=5)

    output_text = tk.Text(output_frame, height=12, width=55)
    scrollbar = ttk.Scrollbar(output_frame, orient='vertical', command=output_text.yview)
    output_text.configure(yscrollcommand=scrollbar.set)
    output_text.pack(side='left', fill='both', expand=True)
    scrollbar.pack(side='right', fill='y')

    def display_output(text):
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, text)

    def list_students():
        if not system._students.items:
            display_output("No students found!")
            return
        text = "Student List:\n" + "-" * 40 + "\n"
        for s in system._students.items:
            text += f"ID: {s.id}, Name: {s.name}, DoB: {s.dob}\n"
        display_output(text)

    def list_courses():
        if not system._courses.items:
            display_output("No courses found!")
            return
        text = "Courses List:\n" + "-" * 40 + "\n"
        for c in system._courses.items:
            text += f"ID: {c.id}, Name: {c.name}, Credits: {c.credits}\n"
        display_output(text)

    def show_marks():
        if not system._courses.items:
            display_output("No courses found!")
            return

        course_id = simpledialog.askstring("Select Course", "Enter Course ID:", parent=root)
        if not course_id:
            return

        course_marks = system._mark_manager.get_course_marks(course_id)
        if course_marks:
            text = f"Marks for course: {course_id}\n" + "-" * 40 + "\n"
            for student in system._students.items:
                mark = system._mark_manager.get_mark(course_id, student.id)
                if mark is not None:
                    text += f"Student: {student.name} - Mark: {mark}\n"
                else:
                    text += f"Student: {student.name} - Mark: Not Found\n"
            display_output(text)
        else:
            display_output("No marks found for this course!")

    def show_gpa():
        if not system._students.items:
            display_output("No students found!")
            return

        student_id = simpledialog.askstring("Select Student", "Enter Student ID:", parent=root)
        if not student_id:
            return

        student = system._students.find_by_id(student_id)
        if student:
            gpa = system.calculate_student_gpa(student_id)
            display_output(f"Student: {student.name} (ID: {student.id})\nWeighted GPA: {gpa}")
        else:
            display_output("Student not found!")

    def sort_by_gpa():
        if not system._students.items:
            display_output("No students found!")
            return

        student_gpa_list = []
        for student in system._students.items:
            gpa = system.calculate_student_gpa(student.id)
            student_gpa_list.append((student, gpa))

        gpas = np.array([item[1] for item in student_gpa_list])
        sorted_indices = np.argsort(-gpas)

        text = "Students Sorted by GPA (Descending):\n" + "-" * 40 + "\n"
        text += f"{'Rank':<6}{'ID':<12}{'Name':<20}{'GPA':<10}\n"
        for rank, idx in enumerate(sorted_indices, 1):
            student, gpa = student_gpa_list[idx]
            text += f"{rank:<6}{student.id:<12}{student.name:<20}{gpa:<10}\n"
        display_output(text)

    # Button Frame
    btn_frame = ttk.Frame(root)
    btn_frame.pack(fill='x', padx=10, pady=10)

    ttk.Button(btn_frame, text="Setup (Add Students/Courses)",
               command=lambda: system.setup_gui(root)).grid(row=0, column=0, padx=5, pady=5)
    ttk.Button(btn_frame, text="List Students",
               command=list_students).grid(row=0, column=1, padx=5, pady=5)
    ttk.Button(btn_frame, text="List Courses",
               command=list_courses).grid(row=0, column=2, padx=5, pady=5)

    ttk.Button(btn_frame, text="Input Marks",
               command=lambda: system.input_marks_gui(root)).grid(row=1, column=0, padx=5, pady=5)
    ttk.Button(btn_frame, text="Show Marks",
               command=show_marks).grid(row=1, column=1, padx=5, pady=5)
    ttk.Button(btn_frame, text="Show GPA",
               command=show_gpa).grid(row=1, column=2, padx=5, pady=5)

    ttk.Button(btn_frame, text="Sort by GPA",
               command=sort_by_gpa).grid(row=2, column=0, padx=5, pady=5)
    ttk.Button(btn_frame, text="Exit",
               command=root.quit).grid(row=2, column=2, padx=5, pady=5)

    root.mainloop()


# Main
if __name__ == "__main__":
    curses.wrapper(curses_main)
