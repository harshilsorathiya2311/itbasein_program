import matplotlib.pyplot as plt
import numpy as np

#plot 1
x = np.array([1,2,3,4,5,6])
y = np.array([10,20,30,40,50,60])

plt.subplot(1,2,1)
plt.plot(x,y)
plt.title("Plot 1")


#plot 2
x1 = np.array([1,2,3,4,5,6])
y1 = np.array([50,60,30,10,70,80])

plt.subplot(1,2,2)
plt.plot(x1,y1)
plt.title("Plot 2")

plt.show()