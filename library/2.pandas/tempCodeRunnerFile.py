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

#avrage
avrage = students['marks'].mean()
print("student avrage:")
print(avrage)

#min marks
min = students['marks'].min()
print("student min:")
print(min)

#max marks
max = students['marks'].max()
print("student max:")
print(max)
