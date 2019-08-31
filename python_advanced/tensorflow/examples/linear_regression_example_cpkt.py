
import tensorflow as tf
from tensorflow.contrib import learn
from tensorflow.contrib.learn.python.learn.estimators import model_fn as model_fn_lib
import numpy as np
import os.path

###########################################################################
#### Hyper-params and save file
############################################################################

DIRECTORY_SAVERS = "./checkpoints/linear_regression_example_cpkt/"
CPKT_FILE_NAME = "linear_regression"
n_epochs = 20

############################################################################
#### Create data
############################################################################

x = np.arange(100, step=0.1)
y = x + 3 * np.cos(x/5)  
n_samples = 1000
batch_size = 10

# rewrite as column vector
x = np.reshape(x, (n_samples, 1))
y = np.reshape(y, (n_samples, 1)) 

############################################################################
#### Define graph
############################################################################

tf.reset_default_graph()
batch_size_ = 10
n_features_ = 1
linear_regression_graph = tf.Graph()
seed_val = 123

with linear_regression_graph.as_default():
    batch_size = batch_size_
    n_features = n_features_
    
    pl_x = tf.placeholder(tf.float32, shape=(batch_size, 1))
    pl_y = tf.placeholder(tf.float32, shape=(batch_size, 1))
    W = tf.get_variable("weights", (1,1), initializer=tf.random_normal_initializer(seed=seed_val))
    b = tf.get_variable("bias", (1,), initializer=tf.constant_initializer(0.))
    y_pred = tf.matmul(pl_x, W) + b    
    loss = tf.reduce_mean((pl_y - y_pred)**2/batch_size)
    
    optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.001).minimize(loss)
    
    # Add allways the  tf.global_variables_initializer() and tf.Saver() in the graph
    init = tf.global_variables_initializer()   
    saver = tf.train.Saver()
    #saver.save(as_default, "./saved_tests/linear_regression_saver.ckpt")


############################################################################
#### Train model in a session
############################################################################

if not os.path.exists(DIRECTORY_SAVERS):
    os.makedirs(DIRECTORY_SAVERS)

indices_batches = [ x for x in range(0, len(x) + 1, 10) ]

with tf.Session(graph=linear_regression_graph) as sess:

    if os.path.exists(DIRECTORY_SAVERS + CPKT_FILE_NAME + ".meta"):
        print("\nCheckpoint found, keep training")
        #tf.reset_default_graph()
        saver.restore(sess, DIRECTORY_SAVERS + CPKT_FILE_NAME) 
    else:
        print("\nCheckpoint not found, start training")
        sess.run(init)

    print("\n\nShow me W and b")
    print("weights before training: ",sess.run([W]))
    print("bias before training: ",sess.run([b]), "\n")
    
    for epoch in range(n_epochs):
        mean_loss = []
        for b_beg, b_end in zip(indices_batches[0:-1], indices_batches[1:]):
            _, l = sess.run([optimizer, loss], feed_dict={pl_x: x[b_beg:b_end], 
                                                          pl_y: y[b_beg:b_end]})
            mean_loss.append(l)
        print("epoch: ", epoch, " loss: ", np.mean(mean_loss))
    
    print("\n\nShow me W and b")
    print("weights after training: ",sess.run([W]))
    print("bias after training: ",sess.run([b]), "\n")

    #tf.train.export_meta_graph(DIRECTORY_SAVERS  + CPKT_FILE_NAME)
    saver.save(sess, DIRECTORY_SAVERS + CPKT_FILE_NAME)
