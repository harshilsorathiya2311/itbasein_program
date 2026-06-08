#Project 3: Weather Analysis
import numpy as np

# temperature in array
temp = np.array([30, 32, 28, 35, 31])
print("temperature:", temp)

# Calculate average temperature
average_temp = np.mean(temp)
print("average temperature:", average_temp)

# Calculate highest and lowest temperature
highest = np.max(temp)
print("highest temperature:", highest)

lowest = np.min(temp)
print("lowest temperature:", lowest)

#hot days 
hot_days = temp[temp > 30]
print("hot days:", hot_days)