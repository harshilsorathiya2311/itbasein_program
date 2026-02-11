numbers = [2, 5, 8, 9, 6, 3, 5, 9, 5]

most_repeated = numbers[0]

for i in numbers:
    count = 0
    for j in numbers:
        if i == j:
            count += 1

print("Most Repeated Number:", most_repeated)

