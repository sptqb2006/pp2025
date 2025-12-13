import curses
import numpy as np

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


# Main
if __name__ == "__main__":
    print("Select mode:")
    print("1. Standard Console Mode")
    print("2. Curses UI Mode")
    mode = input("Enter choice (1/2): ")

    system = StudentMarkSystem()

    if mode == '2':
        curses.wrapper(out.curses_main, system)
    else:
        system.setup()
        system.run()
