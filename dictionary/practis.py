data = [
    {
    'name':'csk',
    'count':3
    },
    {
    'name':'mi',
    'count':1
    },
    {
    'name':'rcb',
    'count':5
    },
]

for i in range(len(data)):
    for j in range(i+1, len(data)):
        if data[j]['count'] > data[i]['count']:
            data[i], data[j] = data[j], data[i]

print(data)