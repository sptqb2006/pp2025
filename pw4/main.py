import curses
import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

from domains import Student, Course, MarkManager, EntityCollection
import input as inp
import output as out


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
        inp.input_students(self._students)
        inp.input_courses(self._courses)

    def list_students(self):
        self._students.list_all("Student List")

    def list_courses(self):
        self._courses.list_all("Courses list")

    def input_marks(self):
        inp.input_marks_for_course(self._students, self._courses, self._mark_manager)

    def show_student_marks(self):
        print("\n--- Show Marks ---")
        course_id = inp.get_course_id_input(self._courses)
        out.print_course_marks(course_id, self._students, self._mark_manager)

    def calculate_student_gpa(self, student_id):
        """Calculate average GPA for a given student using weighted sum of credits and marks"""
        marks_array, course_ids = self._mark_manager.get_student_marks_array(student_id)

        if len(marks_array) == 0:
            return 0.0

        credits_list = []
        for cid in course_ids:
            course = self._courses.find_by_id(cid)
            if course:
                credits_list.append(course.credits)
            else:
                credits_list.append(0)

        credits_array = np.array(credits_list)

        total_credits = np.sum(credits_array)
        if total_credits == 0:
            return 0.0

        weighted_sum = np.sum(marks_array * credits_array)
        gpa = weighted_sum / total_credits

        return round(gpa, 2)

    def show_student_gpa(self):
        """Show GPA for a specific student"""
        print("\n**** Student GPA ****")
        student_id = inp.get_student_id_input(self._students)

        student = self._students.find_by_id(student_id)
        if student is None:
            print("Student not found!")
            return

        gpa = self.calculate_student_gpa(student_id)
        out.print_student_gpa(student, gpa)

    def sort_students_by_gpa(self):
        """Sort student list by GPA descending"""
        student_gpa_list = []
        for student in self._students.items:
            gpa = self.calculate_student_gpa(student.id)
            student_gpa_list.append((student, gpa))
        out.print_sorted_students(student_gpa_list)

    def run(self):
        """Main menu loop"""
        while True:
            out.print_header()
            out.print_menu()
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


# Tkinter GUI Main
def tkinter_main():
    """Tkinter GUI main"""
    root = tk.Tk()
    root.title("USTH Student Mark Management System v4.0")
    root.geometry("500x450")

    system = StudentMarkSystem()

    # Header
    header_frame = ttk.Frame(root)
    header_frame.pack(fill='x', padx=10, pady=10)
    ttk.Label(header_frame, text="USTH STUDENT MARK MANAGEMENT SYSTEM v4.0",
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

    def setup_gui():
        """Setup students and courses via GUI"""
        inp.input_students_gui(system._students, root)
        inp.input_courses_gui(system._courses, root)
        display_output("Setup complete! Students and courses added.")

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

    def input_marks():
        inp.input_marks_for_course_gui(system._students, system._courses, system._mark_manager, root)

    def show_marks():
        if not system._courses.items:
            display_output("No courses found!")
            return

        course_id = inp.get_course_id_input_gui(system._courses, root)
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

        student_id = inp.get_student_id_input_gui(system._students, root)
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
               command=setup_gui).grid(row=0, column=0, padx=5, pady=5)
    ttk.Button(btn_frame, text="List Students",
               command=list_students).grid(row=0, column=1, padx=5, pady=5)
    ttk.Button(btn_frame, text="List Courses",
               command=list_courses).grid(row=0, column=2, padx=5, pady=5)

    ttk.Button(btn_frame, text="Input Marks",
               command=input_marks).grid(row=1, column=0, padx=5, pady=5)
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
    system = StudentMarkSystem()
    curses.wrapper(out.curses_main, system)
