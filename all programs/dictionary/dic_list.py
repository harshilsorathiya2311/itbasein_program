numbers = [1, 2, 3, 2, 2, 1, 2, 2, 1, 3]

count_dict = {}

for num in numbers:
    count_dict[num] = count_dict.get(num, 0) + 1

print(count_dict)
