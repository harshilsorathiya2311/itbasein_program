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

data = ["mountainA", 10, 5, "ahd"],["mountainB", 5, 20, "surat"],["mountainC", 7, 30, "mumbai"]
data = [["MountA","MountinB","MountainC"], [10,12,15], [4,3,12], ["ahd","ahd","ahd"]]


# task 2

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



# task 3
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



# task 3
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


# task 4
data = [
    ["MountainA","MountainB","MountainC","MountainD","MountainE"],
    [10,20,30,40,50,60,70,80,90],  
    [2,4,6,8,],       
    ["ahd","mumbai"]   
]

#output
('MountainA', {'height': 10, 'width': 2, 'location': 'ahd'})
('MountainB', {'height': 20, 'width': 4, 'location': 'mumbai'})
('MountainC', {'height': 30, 'width': 6, 'location': 'Not available'})
('MountainD', {'height': 40, 'width': 8, 'location': 'Not available'})
('MountainE', {'height': 50, 'width': 0, 'location': 'Not available'})
('Not available', {'height': 60, 'width': 0, 'location': 'Not available'})
('Not available', {'height': 70, 'width': 0, 'location': 'Not available'})
('Not available', {'height': 80, 'width': 0, 'location': 'Not available'})
('Not available', {'height': 90, 'width': 0, 'location': 'Not available'})


data = [
    ["MountainA", "MountainB", "MountainC", "MountainD", "MountainE"],
    [10, 20, 30, 40, 50, 60, 70, 80, 90],  
    [2, 4, 6, 8],       
    ["ahd", "mumbai"]   
]

names, heights, widths, locations = data

dic_text = []

for i in range(len(heights)):

    if i < len(names):
        name = names[i]
    else:
        name = "Not available"


    if i < len(widths):
        width = widths[i]
    else:
        width = 0


    if i < len(locations):
        location = locations[i]
    else:
        location = "Not available"
    

    dic_text.append((name, {'height': heights[i], 'width': width, 'location': location}))


for item in dic_text:
    print(item)
    
    
    
   
#task 5 
    
n = int(input("Enter total values: "))

nums = []
for i in range(n):
    nums.append(int(input("Enter value: ")))

odd = []
even = []

# Separate odd and even
for i in nums:
    if i % 2 == 0:
        even.append(i)
    else:
        odd.append(i)

# Find largest & smallest odd
largest_odd = odd[0]
smallest_odd = odd[0]

for i in odd:
    if i > largest_odd:
        largest_odd = i
    if i < smallest_odd:
        smallest_odd = i

# Find largest & smallest even
largest_even = even[0]
smallest_even = even[0]

for i in even:
    if i > largest_even:
        largest_even = i
    if i < smallest_even:
        smallest_even = i

# Find most repeated number
max_count = 0
most_repeated = nums[0]

for i in nums:
    count = 0
    for j in nums:
        if i == j:
            count += 1
    if count > max_count:
        max_count = count
        most_repeated = i

# Single print at the end
print({
    "odd": odd,
    "even": even,
    "largest_odd": largest_odd,
    "largest_even": largest_even,
    "smallest_odd": smallest_odd,
    "smallest_even": smallest_even,
    "most_repeated_num": most_repeated
})


# 6  

n = int(input("Enter total values: "))

nums = []
for i in range(n):
    nums.append(int(input("Enter value: ")))

odd = []
even = []

# Separate odd & even
for i in nums:
    if i % 2 == 0:
        even.append(i)
    else:
        odd.append(i)

# -------- Odd calculations --------
if len(odd) > 0:
    largest_odd = odd[0]
    smallest_odd = odd[0]

    for i in odd:
        if i > largest_odd:
            largest_odd = i
        if i < smallest_odd:
            smallest_odd = i
else:
    largest_odd = None
    smallest_odd = None

# -------- Even calculations --------
if len(even) > 0:
    largest_even = even[0]
    smallest_even = even[0]

    for i in even:
        if i > largest_even:
            largest_even = i
        if i < smallest_even:
            smallest_even = i
else:
    largest_even = None
    smallest_even = None

# -------- Most repeated number --------
max_count = 0
most_repeated = None

for i in nums:
    count = 0
    for j in nums:
        if i == j:
            count += 1

    if count > max_count:
        max_count = count
        most_repeated = i

# -------- Single Print --------
print({
    "odd": odd,
    "even": even,
    "largest_odd": largest_odd,
    "largest_even": largest_even,
    "smallest_odd": smallest_odd,
    "smallest_even": smallest_even,
    "most_repeated_num": most_repeated
})

