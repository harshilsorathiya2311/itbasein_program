data = [
    ["MountainA","MountainB","MountainC","MountainD","MountainE"],
    [10,20,30,40,50,60,70,80,90],  
    [2,4,6,8,],       
    ["ahd","mumbai"]   
]

names, heights, widths, locations = data

dic_text = []

for i in range(len(heights)):
    name = names[i] if i < len(names) else "Not available"
    width = widths[i] if i < len(widths) else 0
    location = locations[i] if i < len(locations) else 'Not available'
    
    dic_text.append((name, {'height': heights[i], 'width': width, 'location': location}))

for item in dic_text:
    print(item)