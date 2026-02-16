ipl = [
    {'team_A': 'mi',
    'cup': 3},
    {'team_A': 'csk',
     'cup': 5},
    {'team_A': 'rcb', 
     'cup': 1}
]

for i in range(len(ipl)):
    for j in range(i+1,len(ipl)):
        if ipl[j]['cup'] > ipl[i]['cup']:
            ipl[i], ipl[j] = ipl[j], ipl[i]
            
print(ipl)
        
        