import tensorflow as tf

# Create a scalar tensor.
scalar = tf.constant(5)
print(scalar)

#Create a 1D tensor (vector) with values [1, 2, 3, 4].
vector = tf.constant([1, 2, 3, 4])
print(vector)   

#Create a 2D tensor (matrix) with values [[1, 2], [3, 4]].
matrix = tf.constant([[1, 2], [3, 4]])      
print(matrix)