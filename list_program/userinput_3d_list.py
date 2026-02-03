a = []
b = []
c = []

a = input("enter a value:").split()
b = input("enter b value:").split()
c = input("enter c value:").split()

x = [a,b,c]
print(x)


for i in x:
    for j in i:
        print(j)
    print(i)
