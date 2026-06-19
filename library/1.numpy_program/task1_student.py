# Project 1: Student Marks Analysis
import numpy as np

#store marks in array
marks = np.array([50, 75, 31, 90, 60])
print("marks",marks)

# Calculate average marks
average = np.mean(marks)
print("average marks:", average)

# Calculate highest marks
highest =np.max(marks)
print("highest marks:",highest)

# Calculate lowest marks
lowest = np.min(marks)  
print("lowest marks:", lowest)

#pass or fail
pass_fail = np.where(marks >= 33, "pass", "fail")
print("pass or fail:", pass_fail)

