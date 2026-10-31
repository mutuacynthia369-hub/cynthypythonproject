import json
import os
from datetime import datetime


class Student:

    def __init__(self, admission_no, name, age, course):
        self.admission_no = admission_no
        self.name = name
        self.age = age
        self.course = course
        self.marks = {}
        self.attendance = []

    def add_marks(self, subject, mark):

        if mark < 0 or mark > 100:
            print("Marks must be between 0 and 100.")
            return False

        self.marks[subject] = mark
        return True

    def calculate_average(self):

        if not self.marks:
            return 0

        return sum(self.marks.values()) / len(self.marks)

    def calculate_grade(self):

        average = self.calculate_average()

        if average >= 70:
            return "A"
        elif average >= 60:
            return "B"
        elif average >= 50:
            return "C"
        elif average >= 40:
            return "D"
        else:
            return "E"

    def mark_attendance(self, status):

        record = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "status": status
        }

        self.attendance.append(record)

    def to_dict(self):

        return {
            "admission_no": self.admission_no,
            "name": self.name,
            "age": self.age,
            "course": self.course,
            "marks": self.marks,
            "attendance": self.attendance
        }

    @classmethod
    def from_dict(cls, data):

        student = cls(
            data["admission_no"],
            data["name"],
            data["age"],
            data["course"]
        )

        student.marks = data["marks"]
        student.attendance = data["attendance"]

        return student




class Teacher:

    def __init__(self, teacher_id, name, subject):
        self.teacher_id = teacher_id
        self.name = name
        self.subject = subject

    def to_dict(self):

        return {
            "teacher_id": self.teacher_id,
            "name": self.name,
            "subject": self.subject
        }



class School:

    def __init__(self):

        self.students = {}
        self.teachers = {}

        self.load_data()

    

    def save_data(self):

        data = {
            "students": {
                key: student.to_dict()
                for key, student in self.students.items()
            },

            "teachers": {
                key: teacher.to_dict()
                for key, teacher in self.teachers.items()
            }
        }

        with open("school_data.json", "w") as file:
            json.dump(data, file, indent=4)

    def load_data(self):

        if not os.path.exists("school_data.json"):
            return

        try:
            with open("school_data.json", "r") as file:
                data = json.load(file)

            for key, value in data.get("students", {}).items():
                self.students[key] = Student.from_dict(value)

            for key, value in data.get("teachers", {}).items():
                self.teachers[key] = Teacher(
                    value["teacher_id"],
                    value["name"],
                    value["subject"]
                )

        except (json.JSONDecodeError, KeyError, TypeError):
            print("Could not load school records.")



    def register_student(self):

        print("\n===== STUDENT REGISTRATION =====")

        admission = input("Admission number: ").strip()

        if not admission:
            print("Admission number cannot be empty.")
            return

        if admission in self.students:
            print("Student already registered.")
            return

        name = input("Student full name: ").strip()

        if not name:
            print("Name cannot be empty.")
            return

        try:
            age = int(input("Student age: "))

            if age < 1 or age > 100:
                print("Enter a valid age.")
                return

        except ValueError:
            print("Age must be a number.")
            return

        course = input("Enter course: ").strip()

        if not course:
            print("Course cannot be empty.")
            return

        student = Student(admission, name, age, course)

        self.students[admission] = student

        self.save_data()

        print("\nStudent registered successfully!")


    def register_teacher(self):

        print("\n===== TEACHER REGISTRATION =====")

        teacher_id = input("Teacher ID: ").strip()

        if not teacher_id:
            print("Teacher ID cannot be empty.")
            return

        if teacher_id in self.teachers:
            print("Teacher already registered.")
            return

        name = input("Teacher name: ").strip()
        subject = input("Subject taught: ").strip()

        if not name or not subject:
            print("All fields are required.")
            return

        teacher = Teacher(teacher_id, name, subject)

        self.teachers[teacher_id] = teacher

        self.save_data()

        print("Teacher registered successfully!")

    

    def view_students(self):

        print("\n===== REGISTERED STUDENTS =====")

        if not self.students:
            print("No students registered.")
            return

        for student in self.students.values():

            print("----------------------------")
            print("Admission:", student.admission_no)
            print("Name:", student.name)
            print("Age:", student.age)
            print("Course:", student.course)



    def view_teachers(self):

        print("\n===== REGISTERED TEACHERS =====")

        if not self.teachers:
            print("No teachers registered.")
            return

        for teacher in self.teachers.values():

            print("----------------------------")
            print("Teacher ID:", teacher.teacher_id)
            print("Name:", teacher.name)
            print("Subject:", teacher.subject)

    

    def search_student(self):

        admission = input(
            "Enter admission number: "
        ).strip()

        student = self.students.get(admission)

        if student:

            print("\nStudent found!")
            print("Name:", student.name)
            print("Age:", student.age)
            print("Course:", student.course)

        else:
            print("Student not found.")


    def update_student(self):

        admission = input("Enter admission number: ")

        student = self.students.get(admission)

        if not student:
            print("Student not found.")
            return

        print("1. Update name")
        print("2. Update age")
        print("3. Update course")

        choice = input("Choose field: ")

        if choice == "1":

            name = input("New name: ").strip()

            if name:
                student.name = name

        elif choice == "2":

            try:
                age = int(input("New age: "))

                if age < 1 or age > 100:
                    print("Invalid age.")
                    return

                student.age = age

            except ValueError:
                print("Invalid age.")
                return

        elif choice == "3":

            course = input("New course: ").strip()

            if course:
                student.course = course

        else:
            print("Invalid choice.")
            return

        self.save_data()

        print("Student details updated!")


    def delete_student(self):

        admission = input("Enter admission number: ")

        if admission not in self.students:
            print("Student not found.")
            return

        confirm = input(
            "Are you sure you want to delete? (yes/no): "
        ).lower()

        if confirm == "yes":

            del self.students[admission]

            self.save_data()

            print("Student deleted successfully!")

        else:
            print("Deletion cancelled.")


    def record_marks(self):

        admission = input("Enter admission number: ")

        student = self.students.get(admission)

        if not student:
            print("Student not found.")
            return

        subject = input("Enter subject: ").strip()

        if not subject:
            print("Subject cannot be empty.")
            return

        try:
            mark = float(input("Enter marks (0-100): "))

            if student.add_marks(subject, mark):

                self.save_data()

                print("Marks recorded successfully!")

        except ValueError:
            print("Enter valid numerical marks.")

    def student_report(self):

        admission = input("Enter admission number: ")

        student = self.students.get(admission)

        if not student:
            print("Student not found.")
            return

        print("\n========== STUDENT REPORT ==========")

        print("Name:", student.name)
        print("Admission:", student.admission_no)
        print("Course:", student.course)

        print("\nSUBJECT RESULTS")

        if not student.marks:
            print("No marks recorded.")

        else:

            for subject, mark in student.marks.items():
                print(subject, ":", mark)

            print(
                "Average:",
                round(student.calculate_average(), 2)
            )

            print("Grade:", student.calculate_grade())

        print("====================================")


    def record_attendance(self):

        admission = input("Enter admission number: ")

        student = self.students.get(admission)

        if not student:
            print("Student not found.")
            return

        print("1. Present")
        print("2. Absent")

        choice = input("Choose attendance status: ")

        if choice == "1":
            status = "Present"

        elif choice == "2":
            status = "Absent"

        else:
            print("Invalid choice.")
            return

        student.mark_attendance(status)

        self.save_data()

        print("Attendance recorded successfully!")


    def view_attendance(self):

        admission = input("Enter admission number: ")

        student = self.students.get(admission)

        if not student:
            print("Student not found.")
            return

        print("\n===== ATTENDANCE RECORD =====")

        if not student.attendance:
            print("No attendance records.")
            return

        for record in student.attendance:

            print(
                record["date"],
                "-",
                record["status"]
            )


def main():

    school = School()

    while True:

        print("\n")
        print("**************************************")
        print("       SCHOOL MANAGEMENT SYSTEM")
        print("**************************************")

        print("1. Register Student")
        print("2. Register Teacher")
        print("3. View Students")
        print("4. View Teachers")
        print("5. Search Student")
        print("6. Update Student")
        print("7. Delete Student")
        print("8. Record Marks")
        print("9. Student Report")
        print("10. Record Attendance")
        print("11. View Attendance")
        print("12. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            school.register_student()

        elif choice == "2":
            school.register_teacher()

        elif choice == "3":
            school.view_students()

        elif choice == "4":
            school.view_teachers()

        elif choice == "5":
            school.search_student()

        elif choice == "6":
            school.update_student()

        elif choice == "7":
            school.delete_student()

        elif choice == "8":
            school.record_marks()

        elif choice == "9":
            school.student_report()

        elif choice == "10":
            school.record_attendance()

        elif choice == "11":
            school.view_attendance()

        elif choice == "12":
            print("Thank you for using the system!")
            break

        else:
            print("Invalid choice. Try again.")


# ==========================================
# 5. RUN PROGRAM
# ==========================================

if __name__ == "__main__":
    main()