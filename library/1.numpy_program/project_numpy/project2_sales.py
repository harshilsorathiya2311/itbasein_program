#project 2: Sales Analysis

import numpy as np
import matplotlib.pyplot as plt

# product names
products = np.array(["laptop", "phone", "tablet", "tv", "smartwatch"])
print("products_name", products)

# sales 
sales = np.array([25000, 23000, 35000, 40000, 35000])
print("sales", sales)

# calculate total sales
total_sales = np.sum(sales)
print("total sales:", total_sales)

# calculate average sales
average_sales = np.mean(sales)
print("average sales:",average_sales)

# calculate highest 
highest_sales =np.max(sales)
print("highest sales:", highest_sales)

# calculate lowest sales
lowest_sales = np.min(sales)
print("lowest sales:", lowest_sales)

#best_selling_product
best_product = products[np.argmax(sales)]
print("besst_selling_product:", best_product)

#lowest selling product
lowest_product = products[np.argmin(sales)]
print("lowest_selling:", lowest_product)

# plt.plot(products,sales)
# plt.show()
