students = []
courses = []
marks = {}

#Input number of students in a class
def input_num_of_students(): #I
    count = int(input("Enter number of students: "))
    return count

#Input student information: id, name, DoB
def input_student_info():

    print("\n**** Input student information: id, name, DoB ****")
    sid = input("Enter student ID: ")
    name = input("Enter student name: ")
    dob = input("Enter student DoB: ")

#Dictionary
    student = {
        'id': sid,
        'name': name,
        'dob': dob
    }
    students.append(student)
#Input number of courses
def input_num_course():
    count = int(input("Enter number of courses: "))
    return count
 
#Input course information
def input_course_info():

    print("\n**** Input Course Information ****")
    cid = input("Enter Course ID: ")
    nameC = input("Enter Course Name: ")
#Dictionary
    course = {
        'id': cid,
        'nameC': nameC
    }
    courses.append(course)

#List courses
def list_courses():
    print("\n**** Courses list ****")
    for c in courses:
        print(f"ID: {c['id']}, Name: {c['nameC']}")

#List student
def list_student():
    print("\n**** Student List ****")
    for s in students:
        print(f"ID: {s['id']}, Name: {s['name']}, DoB: {s['dob']}")

#Input mark
def input_marks():
    print("\n**** Input Marks ****")
    list_courses()
    selected_course = input("Select Course ID to input marks: ")

    if selected_course not in [c['id'] for c in courses]: #check if exits (or not)
        print("Course not found!")
        return
    
    if selected_course not in marks: #if not exits -> create dictionary
        marks[selected_course] = {}

    for s in students:
        mark = float(input(f"Enter mark for student {s['name']} (ID: {s['id']}): "))
        marks[selected_course][s['id']] = mark

#Show student marks
def show_student_marks():
    print("\n--- Show Marks ---")
    list_courses()
    selected_course = input("Select Course ID to view marks: ")

    if selected_course in marks:
        print(f"Mark for course: {selected_course}")
        for s in students:
            if s['id'] in marks[selected_course]:
                print(f"Student: {s['name']} - Mark: {marks[selected_course][s['id']]}")
            else:
                print(f"Student: {s['name']} - mark: Not Found")

#Main
if __name__ == "__main__":
    num_students = input_num_of_students()
    for _ in range(num_students):
        input_student_info()

    num_courses = input_num_course()
    for _ in range(num_courses):
        input_course_info()

    while True:
        print("\n===========================================================")
        print("USTH STUDENT MARK MANAGEMENT SYSTEM v1.0_Release by SPTQB_2006")
        print("1. List Students")
        print("2. List Courses")
        print("3. Input Marks for a Course")
        print("4. Show Marks for a Course")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            list_student()
        elif choice == '2':
            list_courses()
        elif choice == '3':
            input_marks()
        elif choice == '4':
            show_student_marks()
        elif choice == '5':
            break
        else:
            print("Invalid choice!")