# task 1
out_put = {
    "mountianA":{
        "weidth":10,
        "height":5,
        "location":"ahd",
    },
    "mountianA":{   
        "height":5,
        "weidth":10,
        "location":"ahd",
    },
    "mountianA":{
        "height":5,
        "weidth":10,
        "location":"ahd",
    },
}

data = [[mountainA,10,5,ahd],[mountainA,10,5,ahd],[mountainA,10,5,ahd]]
data = [[MountA,MountinB,MountainC],[10,12,15],[4,3,12],[ahd,ahd,ahd]]




data = [["MountA","MountinB","MountainC","MountainD","MountainE"],
        [10,12,15,25],
        [4,3,12],
        ["ahd","ahd",]]
dic_text = {}

for name, width, height, location in zip(data[0],data[1],data[2],data[3]):
    
    dic_text[name] = {
        "width": width,
        "height": height,
        "location": location
    }
print(dic_text)



#output
names = ["MountainA","MountainB","MountainC","MountainD","MountainE"]
widths = [10,12,15,25]
heights = [4,3,12]
locations = ["ahd","ahd"]

dic_text = {}

for i in range(len(names)):
    dic_text[names[i]] = {
        "width": widths[i] if i < len(widths) else 0,
        "height": heights[i] if i < len(heights) else 0,
        "location": locations[i] if i < len(locations) else "Not found"
    }

print(dic_text)




data = [
    ["MountainA","MountainB","MountainC","MountainD","MountainE"],  # names
    [10,12,15,25],   # widths
    [4,3,12],        # heights
    ["ahd","ahd"]    # locations
]

dic_text = {}

names = data[0]
widths = data[1]
heights = data[2]
locations = data[3]

for i, name in enumerate(names):
    # Use the value if exists, otherwise default
    width = widths[i] if i < len(widths) else 0
    height = heights[i] if i < len(heights) else 0
    location = locations[i] if i < len(locations) else "Not found"
    
    dic_text[name] = {
        "width": width,
        "height": height,
        "location": location
    }

print(dic_text)