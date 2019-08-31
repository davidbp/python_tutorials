import tensorflow as tf

def load_graph():

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

    return linear_regression_graph