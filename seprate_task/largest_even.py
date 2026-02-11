numbers = [2, 5, 8, 9, 6, 3]

large_even = None

for num in numbers:
    if num % 2 == 0:                  
        if large_even is None:    
            large_even = num
        else:
            if num > large_even: 
                large_even = num

print("large even value",large_even)
