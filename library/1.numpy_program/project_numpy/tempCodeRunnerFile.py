import numpy as np

products = np.array(["laptop","tv","smartwatch"])
print(products)

#sales
sales = np.array([5000,41000,60000])
print(sales)

#max
max = np.max(sales)
print(max)

#min
min = np.min(sales)
print(min)

sum = np.sum(sales)
print(sum)

best = products[np.argmax(sales)]
print(best)