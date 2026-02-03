a = [1,2,3]
b = ['a','b','c']
c = [a,b]

print(c)
for i in c:
    for j in i:
        print(j)
    print(i)