seprate = [2, 5, 8, 9, 6, 3]

even = []
odd = []

for num in seprate:
    if num % 2 == 0:
        even.append(num)
    else:
        odd.append(num)
        
print(seprate)
print("even",even)
print("odd",odd)
