n = int(input("enter total value: "))

empty = []
for i in range(n):
    empty.append(int(input("enter value: ")))

odd = []
even = []

# even or odd
for i in empty:
    if i % 2 == 0:
        even.append(i)
    else:
        odd.append(i)
        
#large and small even 
if len(even) > 0:
    
    large_even = even[0]
    small_even = even[0]
    
    for i in even:
        
        if i > large_even:
            large_even = i
            
        if i < small_even:
            small_even = i
              
#large and small odd 
if len(odd) > 0:
    
    large_odd = odd[0]
    small_odd = odd[0]
    
    for i in odd:
        
        if i > large_odd:
            large_odd = i
        if i < small_odd:
            small_odd = i   
                
print({
    "odd": odd,
    "even": even,
    "large_even": large_even,
    "large_odd": large_odd,
    "small_even": small_even,
    "small_odd": small_odd,
})
