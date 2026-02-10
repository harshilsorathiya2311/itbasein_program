data = [ 
    ["MountainA","MountainB","MountainC","MountainD","MountainE"],  
    [10,12,15,25],   
    [4,3,12],        
    ["ahd","ahd"]   
]

mountain_hills = {}   

names, widths, heights, locations = data

for i in range(len(names)):
    
#width
    if i < len(widths):
        width = widths[i]
    else:
        width = 0
        
#heights
    if i < len(heights):
        height = heights[i]
    else:
        height = 0

#location
    if i < len(locations):
        location = locations[i]
    else:
        location = "Not found"
    
    
    mountain_hills[names[i]] = {
        "width": width,
        "height": height,
        "location": location
    }

print(mountain_hills)

