numbers = [2, 5, 8, 9, 6, 3]

largest_odd = None

for num in numbers:
    if num % 2 != 0:                 
        if largest_odd is None:     
            largest_odd = num
        else:
            if num > largest_odd:   
                largest_odd = num


print("Large odd value", largest_odd)
