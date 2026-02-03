a = []
b = []
c = []

print("Enter a value:")
for i in range(3):
    a.append(input())

print("Enter b value:")
for i in range(3):
    b.append(input())

print("Enter c value:")
for i in range(3):
    c.append(input())

x = [a, b, c]

print(x)

for i in x:
    for j in i:
        print(j)
    print(i)