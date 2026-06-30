import tensorflow as tf

tensor = tf.constant([[1,2,3],
                    [4,5,6]])
print("shape", tensor.shape)
print("rank", tf.rank(tensor))

