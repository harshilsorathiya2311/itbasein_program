#Project 4: Matrix Calculator
import numpy as np

# Matrix Creation
a = np.array([[1,2],
            [3,4]])

b = np.array([[5,6],
            [7,8]])

# Matrix Addition
addition  = a + b
print("addition:",addition)

# Matrix Subtraction
subtraction = a - b
print("subtraction:", subtraction)

# Matrix Multiplication
multiplication = np.dot(a,b)
print("multiplication:", multiplication)