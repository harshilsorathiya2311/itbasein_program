import tensorflow as tf

# create tensors
a = tf.constant(10)
b = tf.constant(5)

# operations
print("Addition:", tf.add(a, b))
print("Subtraction:", tf.subtract(a, b))
print("Multiplication:", tf.multiply(a, b))
print("Division:", tf.divide(a, b))