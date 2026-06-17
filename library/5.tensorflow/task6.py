#1.Create a tensor containing numbers 1 to 10.
import tensorflow as tf
tensor = tf.constant([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])   
print (tensor)

#2.Add two tensors.
a = tf.constant(20)
b = tf.constant(30)
print(a+b)

#3.Create a tensor filled with zeros.
zeros_tensor = tf.zeros([3, 3])
print(zeros_tensor)

#4.create a tensor filled with ones.
ones_tensor = tf.ones([2,2])
print(ones_tensor)

#5.Generate random values using TensorFlow.
random_tensor = tf.random.normal([2, 2])    
print(random_tensor)

#6.Find the shape of a tensor.  
shape_tensor = tf.shape(random_tensor)
print(shape_tensor)