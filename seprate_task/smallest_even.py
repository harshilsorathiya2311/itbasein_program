numbers = [2, 5, 8, 9, 6, 3]

small_even = None

for num in numbers:
    if num % 2 == 0:                  
        if small_even is None:    
            small_even = num
        else:
            if num < small_even: 
                small_even = num

print("small even value",small_even)
