names = ["MountainA","MountainB","MountainC","MountainD","MountainE"]
widths = [10,12,15,25]
heights = [4,3,12]
locations = ["ahd","ahd"]

dic_text = {}

for i in range(len(names)):
    dic_text[names[i]] = {
        "width": widths[i] if i < len(widths) else 0,
        
        
    
    
    
    dic_text[name] = {
        "width": width,
        "height": height,
        "location": location
    }
print(dic_text)