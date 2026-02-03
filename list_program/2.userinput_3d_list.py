
a = int(input("enter the value of x: "))   
b = int(input("enter the value of y: "))  
c = int(input("enter the value of z: "))  


x = []

for i in range(a):
    layer = []
    print(f"Entering values for Layer {i + 1}:")
    for j in range(b):
        row = []
        for k in range(c):
            value = input(f"Enter value for position [{i}][{j}][{k}]: ")
            row.append(value)
        layer.append(row)
    x.append(layer)


print("The 3D list is:")
print(x)
