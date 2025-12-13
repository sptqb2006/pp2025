import math
import numpy as np


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
