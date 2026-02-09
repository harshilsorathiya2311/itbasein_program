data = [ 
    ["MountainA","MountainB","MountainC","MountainD","MountainE"],  
    [10,12,15,25],   
    [4,3,12],        
    ["ahd","ahd"]   
]

dic_text = {}

names, widths, heights, locations = data

for i in range(len(names)):
    
    width = widths[i] if i < len(widths) else 0
    height = heights[i] if i < len(heights) else 0
    location = locations[i] if i < len(locations) else "Not found"
    
    dic_text[names[i]] = {
        "width": width,
        "height": height,
        "location": location
    }

print(dic_text)

