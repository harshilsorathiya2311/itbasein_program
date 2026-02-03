r = int(input("Enter number of rows: "))
c = int(input("Enter number of columns: "))

m = []

for i in range(r):
    temp = []
    for j in range(c):
        n = int(input(f"Enter element for row {i+1}, column {j+1}: "))
        temp.append(n)
    m.append(temp)

print("The 2D list (matrix) is:")
for row in m:
    print(row)
