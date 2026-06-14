# Project 2: Sales Analysis
import numpy as np
sales = np.array([2500, 3000, 1500, 4000, 3500])
print("sales", sales)

# Calculate total sales
total_sales = np.sum(sales)
print("total sales:", total_sales)

# Calculate average sales
average_sales = np.mean(sales)
print("average sales:",average_sales)


# Calculate highest 
highest_sales =np.max(sales)
print("highest sales:", highest_sales)

# Calculate lowest sales
lowest_sales = np.min(sales)
print("lowest sales:", lowest_sales)