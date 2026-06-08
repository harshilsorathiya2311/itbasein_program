import numpy as np

#1. one dimensional array
arr = np.array([1,2,4,5,9,])
min = np.min(arr)
print("1.min",min)
print(arr)

print(type(arr))

#2. two dimensional array
arr2 = np.array([[1,2,3],
                 [4,5,6,]])

print("2.two dimensional array:",arr2)

#3. three dimensional array
arr3 =np.array([[1,2,3],
                [4,5,6],
                [7,8,9],
                [10,11,12]])
print("3.three dimensional array:",arr3)
print(arr3.ndim)

#4. check shape
arr4 = np.array([[1,2,3],
                 [4,5,6]])
print("4.shape of array:",arr4.shape)

#5. slicing

arr5 = np.array([10,25,45,85,46,96,12])
print("5.slice array:",arr5[3:6])
