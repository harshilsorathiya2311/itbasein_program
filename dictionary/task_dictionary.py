data = [
    ["mountainA", 10, 5, "ahd"],
    ["mountainB", 5, 20, "surat"],
    ["mountainC", 7, 30, "mumbai"]
]

dic_text = {}

for item in data:
    name, width, height, location = item
    dic_text[name] = {
        "width": width,
        "height": height,
        "location": location
    }


print(dic_text)
