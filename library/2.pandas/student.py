import pandas as pd

# create student dataframe
students = pd.DataFrame({
    "student_id": [101, 102, 103, 104, 105],
    "name": ["amit", "riya", "karan", "priya", "rahul"],
    "marks": [85, 92, 45, 78, 35]
})

# display student data
print("student data:")
print(students)

# calculate average marks
average_marks = students['marks'].mean()
print("average marks:", average_marks)

# find topper
topper = students.loc[students['marks'].idxmax()]
print("topper details:", topper)

# filter failed students
failed_students = students[students['marks'] < 40]
print("failed students:", failed_students)