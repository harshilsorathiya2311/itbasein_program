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

#4.Create an array using `arange()` from 1 to 10.
arr4 = np.arange(1,11)
print("4.array from 1 to 10:",arr4)

#5. check shape
arr5 = np.array([[1,2,3],
                [4,5,6]])
print("5.shape of array:",arr5.shape)

#6. slicing

arr6 = np.array([10,25,45,85,46,96,12])
print("6.slice array:",arr6[3:6])

#7. datatype
arr7 = np.array([1,2,3,4,5])
print("7.data type of array:",arr7.dtype)
