data = [["MountA","MountinB","MountainC"], [10,12,15], [4,3,12], ["ahd","ahd","ahd"]]
dic_text = {}

for name, width, height, location in zip(data[0],data[1],data[2],data[3]):
    
    dic_text[name] = {
        "width": width,
        "height": height,
        "location": location
    }


print(dic_text)


ipl = [
    {'team_A': 'mi',
    'cup': 3},
    {'team_A': 'csk', 'cup': 5},
    
    {'team_A': 'rcb', 'cup': 1}
    
]

for i in range(len(ipl)):
    for j in range(i+1, len(ipl)):
        if ipl[j]['cup'] > ipl[i]['cup']:
            ipl[i], ipl[j] = ipl[j], ipl[i]

for team in ipl:
    print(team)