numbers = [2, 5, 8, 9, 6, 3]

small_odd = None

for num in numbers:
    if num % 2 != 0:                 
        if small_odd is None:     
            small_odd = num
        else:
            if num < small_odd:   
                small_odd = num


print("small odd value", small_odd)
