numbers = [2, 5, 1, 9, 6, 3]

large_even = 0

for num in numbers:
    if num % 2 == 0:                  
        if num > large_even: 
            large_even = num

print("large even value",large_even)
