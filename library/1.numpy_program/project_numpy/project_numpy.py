import numpy as np

#1. Store student names and marks.
names = np.array(['fenil','harshil','bhavy','viral','meet'])
marks = np.array([95,70,90,70,30])

print("student names:", names)
print("student marks:", marks)

#2. Calculate average marks.

average = np.mean(marks)
print("average marks:", average)


#3. Calculate highest marks.
highestmarks = np.max(marks)
print("highest marks:", highestmarks)

#4. Calculate lowest marks.
lowestmarks = np.min(marks)
print("lowest marks:", lowestmarks)

#5. Calculate total marks.
totalmarks = np.sum(marks)
print("total marks:", totalmarks)

#7. find the median 
median_student = np.median(marks)
print("median:", median_student)

#6. pass student
pass_student = np.where(marks >= 33, "pass", "fail")
print(pass_student)

#grade
def calculate_grade(mark):
    if mark >= 90:
        return "a"
    elif mark >= 80:
        return "b"
    elif mark >= 70:
        return "c"
    elif mark >= 60:
        return "d"
    elif mark >= 50:
        return "e"
    else:
        return "f"
    

# print(calculate_grade(90))

# Calculate grades for all students
grades = [calculate_grade(mark) for mark in marks]

print(grades)