import matplotlib.pyplot as plt 
import numpy as np

x_points = np.array([10,30,50,20,60])

plt.plot(x_points, linestyle = 'dotted')
plt.plot(x_points, marker = 'o')
plt.grid()
plt.show()