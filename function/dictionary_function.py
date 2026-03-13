def dictionary_func(data):
    dic_text = {}

    for name, width, height, location in zip(data[0], data[1], data[2], data[3]):
        dic_text[name] = {
            "width": width,
            "height": height,
            "location": location
        }

    return dic_text


data = [["MountA","MountinB","MountainC"], [10,12,15], [4,3,12], ["ahd","ahd","ahd"]]

result = dictionary_func(data)

print(result)