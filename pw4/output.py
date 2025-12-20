import curses
import numpy as np
import input as inp


def safe_addstr(stdscr, row, col, text, attr=0):
    """Safely add string, checking screen bounds"""
    max_y, max_x = stdscr.getmaxyx()
    if row < max_y and col < max_x:
        stdscr.addstr(row, col, text[:max_x - col - 1], attr)


def draw_header(stdscr):
    """Draw the header"""
    attr = curses.color_pair(1) | curses.A_BOLD
    safe_addstr(stdscr, 0, 0, "=" * 60, attr)
    safe_addstr(stdscr, 1, 0, "  USTH STUDENT MARK MANAGEMENT SYSTEM v4.0", attr)
    safe_addstr(stdscr, 3, 0, "=" * 60, attr)


def draw_menu(stdscr):
    """Draw the menu"""
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


def display_sorted_students(stdscr, student_gpa_list):
    """Display students sorted by GPA in curses"""
    max_y, max_x = stdscr.getmaxyx()
    safe_addstr(stdscr, 5, 2, "Students Sorted by GPA (Descending):")
    safe_addstr(stdscr, 6, 2, "-" * 50)
    row = 7

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


def wait_for_key(stdscr):
    """Wait for user to press any key"""
    max_y, max_x = stdscr.getmaxyx()
    prompt_row = min(max_y - 2, 18)
    safe_addstr(stdscr, prompt_row, 2, "Press any key to continue...")
    stdscr.refresh()
    stdscr.getch()


def list_students_curses(stdscr, students):
    """List all students in curses"""
    stdscr.clear()
    draw_header(stdscr)
    max_y, _ = stdscr.getmaxyx()
    safe_addstr(stdscr, 5, 2, "**** Student List ****", curses.color_pair(1))
    safe_addstr(stdscr, 6, 2, "-" * 50)

    if not students.items:
        safe_addstr(stdscr, 7, 2, "No students found.")
    else:
        row = 7
        for s in students.items:
            if row >= max_y - 2:
                break
            safe_addstr(stdscr, row, 2, f"ID: {s.id}, Name: {s.name}, DoB: {s.dob}")
            row += 1


def list_courses_curses(stdscr, courses):
    """List all courses in curses"""
    stdscr.clear()
    draw_header(stdscr)
    max_y, _ = stdscr.getmaxyx()
    safe_addstr(stdscr, 5, 2, "**** Course List ****", curses.color_pair(1))
    safe_addstr(stdscr, 6, 2, "-" * 50)

    if not courses.items:
        safe_addstr(stdscr, 7, 2, "No courses found.")
    else:
        row = 7
        for c in courses.items:
            if row >= max_y - 2:
                break
            safe_addstr(stdscr, row, 2, f"ID: {c.id}, Name: {c.name}, Credits: {c.credits}")
            row += 1


def show_marks_curses(stdscr, students, courses, mark_manager):
    """Show marks for a course in curses"""
    course_id = inp.get_course_id_input_curses(stdscr, courses)
    if not course_id:
        return

    stdscr.clear()
    draw_header(stdscr)
    max_y, _ = stdscr.getmaxyx()
    safe_addstr(stdscr, 5, 2, f"Marks for Course: {course_id}", curses.color_pair(1))
    safe_addstr(stdscr, 6, 2, "-" * 50)

    course_marks = mark_manager.get_course_marks(course_id)
    row = 7
    if course_marks:
        for student in students.items:
            if row >= max_y - 2:
                break
            mark = mark_manager.get_mark(course_id, student.id)
            if mark is not None:
                safe_addstr(stdscr, row, 2, f"{student.name}: {mark}")
            else:
                safe_addstr(stdscr, row, 2, f"{student.name}: Not Found")
            row += 1
    else:
        safe_addstr(stdscr, row, 2, "No marks found for this course!")


def show_gpa_curses(stdscr, students, system):
    """Show GPA for a student in curses"""
    student_id = inp.get_student_id_input_curses(stdscr, students)
    if not student_id:
        return

    student = students.find_by_id(student_id)
    if student is None:
        stdscr.clear()
        draw_header(stdscr)
        safe_addstr(stdscr, 5, 2, "Student not found!", curses.color_pair(4) if curses.has_colors() else 0)
        return

    gpa = system.calculate_student_gpa(student_id)

    stdscr.clear()
    draw_header(stdscr)
    safe_addstr(stdscr, 5, 2, f"Student: {student.name} (ID: {student.id})", curses.color_pair(1))
    safe_addstr(stdscr, 7, 2, f"Weighted GPA: {gpa}", curses.color_pair(3))


def curses_main(stdscr, system):
    """Curses-decorated UI main loop"""
    curses.curs_set(1)
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)

    while True:
        stdscr.clear()
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
            inp.input_students_curses(stdscr, system._students)
            inp.input_courses_curses(stdscr, system._courses)
        elif choice == '1':
            list_students_curses(stdscr, system._students)
            wait_for_key(stdscr)
        elif choice == '2':
            list_courses_curses(stdscr, system._courses)
            wait_for_key(stdscr)
        elif choice == '3':
            inp.input_marks_for_course_curses(stdscr, system._students, system._courses, system._mark_manager)
        elif choice == '4':
            show_marks_curses(stdscr, system._students, system._courses, system._mark_manager)
            wait_for_key(stdscr)
        elif choice == '5':
            show_gpa_curses(stdscr, system._students, system)
            wait_for_key(stdscr)
        elif choice == '6':
            stdscr.clear()
            draw_header(stdscr)
            student_gpa_list = []
            for student in system._students.items:
                gpa = system.calculate_student_gpa(student.id)
                student_gpa_list.append((student, gpa))
            display_sorted_students(stdscr, student_gpa_list)
            wait_for_key(stdscr)
        else:
            stdscr.clear()
            draw_header(stdscr)
            safe_addstr(stdscr, 5, 2, "Invalid choice!", curses.color_pair(4))
            wait_for_key(stdscr)


# Console output functions
def print_header():
    """Print console header"""
    print("\n" + "=" * 60)
    print("  USTH STUDENT MARK MANAGEMENT SYSTEM v4.0")
    print("  OOP + Math + NumPy + Modules by SPTQB_2006")
    print("=" * 60)


def print_menu():
    """Print console menu"""
    print("1. List Students")
    print("2. List Courses")
    print("3. Input Marks for a Course")
    print("4. Show Marks for a Course")
    print("5. Show Student GPA")
    print("6. Sort Students by GPA (Descending)")
    print("7. Exit")
    print("-" * 60)


def print_student_gpa(student, gpa):
    """Print student GPA"""
    print(f"\nStudent: {student.name} (ID: {student.id})")
    print(f"Weighted GPA: {gpa}")


def print_sorted_students(student_gpa_list):
    """Print students sorted by GPA"""
    print("\n**** Students Sorted by GPA (Descending) ****")
    gpas = np.array([item[1] for item in student_gpa_list])
    sorted_indices = np.argsort(-gpas)

    print(f"{'Rank':<6}{'ID':<12}{'Name':<20}{'GPA':<10}")
    print("-" * 48)
    for rank, idx in enumerate(sorted_indices, 1):
        student, gpa = student_gpa_list[idx]
        print(f"{rank:<6}{student.id:<12}{student.name:<20}{gpa:<10}")


def print_course_marks(course_id, students, mark_manager):
    """Print marks for a course"""
    course_marks = mark_manager.get_course_marks(course_id)
    if course_marks:
        print(f"Marks for course: {course_id}")
        for student in students.items:
            mark = mark_manager.get_mark(course_id, student.id)
            if mark is not None:
                print(f"Student: {student.name} - Mark: {mark}")
            else:
                print(f"Student: {student.name} - Mark: Not Found")
    else:
        print("No marks found for this course!")
