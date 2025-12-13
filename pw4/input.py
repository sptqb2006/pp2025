from domains import Student, Course


def input_students(collection):
    """Input multiple students"""
    num_students = int(input("Enter number of students: "))
    collection.input_multiple(Student, num_students)


def input_courses(collection):
    """Input multiple courses"""
    num_courses = int(input("Enter number of courses: "))
    collection.input_multiple(Course, num_courses)


def input_marks_for_course(students, courses, mark_manager):
    """Input marks for a specific course"""
    print("\n**** Input Marks ****")
    courses.list_all("Courses list")
    selected_course = input("Select Course ID to input marks: ")

    if courses.find_by_id(selected_course) is None:
        print("Course not found!")
        return

    for student in students.items:
        mark = float(input(f"Enter mark for student {student.name} (ID: {student.id}): "))
        mark_manager.input_marks(selected_course, student.id, mark)
    print("Marks have been rounded down to 1 decimal place using math.floor()")


def get_student_id_input(students):
    """Get student ID from user"""
    students.list_all("Student List")
    return input("Enter Student ID to calculate GPA: ")


def get_course_id_input(courses):
    """Get course ID from user"""
    courses.list_all("Courses list")
    return input("Select Course ID to view marks: ")
