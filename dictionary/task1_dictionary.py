data = [["MountA","MountinB","MountainC"],
        [10,12,15],
        [4,3,12],
        ["ahd","ahd","ahd"]]
dic_text = {}

for name, width, height, location in zip(data[0],data[1],data[2],data[3]):
    
    dic_text[name] = {
        "width": width,
        "height": height,
        "location": location
    }
print(dic_text)