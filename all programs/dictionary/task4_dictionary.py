data = [
    ["MountainA", "MountainB", "MountainC", "MountainD", "MountainE"],
    [10, 20, 30, 40, 50, 60, 70, 80, 90],  
    [2, 4, 6, 8],       
    ["ahd", "mumbai"]   
]

names, heights, widths, locations = data

dic_text = []

for i in range(len(heights)):
#name
    if i < len(names):
        name = names[i]
    else:
        name = "Not available"

#width
    if i < len(widths):
        width = widths[i]
    else:
        width = 0

#location
    if i < len(locations):
        location = locations[i]
    else:
        location = "Not available"
    

    dic_text.append((name, {'height': heights[i], 'width': width, 'location': location}))


for item in dic_text:
    print(item)