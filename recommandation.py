'''
Created on 9 janv. 2018

@author: N'TIC
'''
import tensorflow as tf
import pandas as pd
import declarations as dec
import numpy as np
import random
import math

def get_rtMatrix(slot):
    
    #df_rtData = pd.read_csv('./dataset/dataset2/databyslot/rtdata_matrix_slot_____'+str(slot)+'.txt',
    df_rtData = pd.read_csv('./dataset/dataset2/databyslot/rtdata_matrix_slot_'+str(slot)+'.txt',
    #df_rtData = pd.read_csv('./dataset/dataset1/rtMatrix.txt',
                          sep='\t',                          
                          index_col=0)
    
    return df_rtData

def corrupt(array, corr):
    """
    Set a fraction ('corr') of the entries in a matrix to zero. May or may not be equivalent to a dropout function in tensorflow.
    """
    array = np.array(array)
    for row in array:
        row[np.random.choice(len(row), int(corr*len(row)))] = 0.0
    return array


def create(x, layer_sizes):

    # Build the encoding layers
    next_layer_input = x

    encoding_matrices = []
    for dim in layer_sizes:
        input_dim = int(next_layer_input.get_shape()[1])

        # Initialize W using random values in interval [-1/sqrt(n) , 1/sqrt(n)]
        W = tf.Variable(tf.random_uniform([input_dim, dim], -1.0 / math.sqrt(input_dim), 1.0 / math.sqrt(input_dim)))

        # Initialize b to zero
        b = tf.Variable(tf.zeros([dim]))

        # We are going to use tied-weights so store the W matrix for later reference.
        encoding_matrices.append(W)

        output = (tf.matmul(next_layer_input,W) + b)

        # the input into the next layer is the output of this layer
        next_layer_input = output

    # The fully encoded x value is now stored in the next_layer_input
    encoded_x = next_layer_input

    # build the reconstruction layers by reversing the reductions
    layer_sizes.reverse()
    encoding_matrices.reverse()


    for i, dim in enumerate(layer_sizes[1:] + [ int(x.get_shape()[1])]) :
        # we are using tied weights, so just lookup the encoding matrix for this step and transpose it
        W = tf.transpose(encoding_matrices[i])
        b = tf.Variable(tf.zeros([dim]))
        output = (tf.matmul(next_layer_input,W) + b)
        next_layer_input = output

    # the fully encoded and reconstructed value of x is here:
    reconstructed_x = next_layer_input

    return {
        'x' : x,
        'encoded': encoded_x,
        'decoded': reconstructed_x,
        'cost' : tf.sqrt(tf.reduce_mean(tf.square(x-reconstructed_x)))
    }


def simple_test():
    
    data = get_rtMatrix(0)
    data = data.fillna(0)
    matrix = data.as_matrix()
        
    for n_neurone in range(2,140):
        sess = tf.Session()
        x = tf.placeholder("float", [None, 4500])
        autoencoder = create(x, [n_neurone])
        init = tf.initialize_all_variables()
        sess.run(init)
        train_step = tf.train.GradientDescentOptimizer(0.05).minimize(autoencoder['cost'])

        
        batch = []
        for j in range(142):
            # pick a random centroid
            val = matrix[j]
            batch.append(val)
        
        best_rmse = 100
        step = -1
        for k in range(5000):       
            sess.run(train_step, feed_dict={x: np.array(batch)})
            rmse = sess.run(autoencoder['cost'], feed_dict={x: batch})
            if best_rmse > rmse:
                best_rmse = rmse
                step = k
                     
        print ("nbr_neurones : ",n_neurone, " step : " ,step ,"RMSE", best_rmse)
            


'''
def simple_test():
    
    
        data = get_rtMatrix()
    #print(data.isnull().values.sum())        
    #data = data.fillna(0)
    #print(data.isnull().values.sum())
        
        matrix = data.as_matrix()
        
    
    #for k in range(0,338):
        
        sess = tf.Session()
        #x = tf.placeholder(tf.float32, [None,4500])
        autoencoder = ae.create([50])
        init = tf.initialize_all_variables()
        sess.run(init)
        learning_rate = 0.01
        #train_step = tf.train.AdamOptimizer(learning_rate).minimize(autoencoder['cost']) 
        train_step = tf.train.RMSPropOptimizer(learning_rate).minimize(autoencoder['cost'])

        
        # do 1000 training steps
        for i in range(1):
            # make a batch of 100:
            batch = []
            for j in range(142):
                val = matrix[j]
                batch.append(val)
            #batch = corrupt(batch, 0.2)
                #print(batch)
            
            sess.run(train_step, feed_dict={autoencoder['x']: np.array(batch)})
            if i % 100 == 0:
                print (k, " cost", sess.run(autoencoder['cost'], feed_dict={autoencoder['x']: batch}))
        #print (i, " original", batch)
        #print (i, " encoded", sess.run(autoencoder['encoded'], feed_dict={x: batch}))
        #print (i, " decoded", sess.run(autoencoder['decoded'], feed_dict={x: batch}))

'''
    
simple_test()
'''
nbr_neurone :  2  step :  4989 cost 3.47303
nbr_neurone :  3  step :  4999 cost 3.29716
nbr_neurone :  4  step :  4717 cost 3.20493
nbr_neurone :  5  step :  4280 cost 3.11697
nbr_neurone :  6  step :  4981 cost 3.0418
nbr_neurone :  7  step :  4677 cost 2.9734
nbr_neurone :  8  step :  4966 cost 2.91338
nbr_neurone :  9  step :  4995 cost 2.85271
nbr_neurone :  10  step :  4983 cost 2.79852
nbr_neurone :  11  step :  4999 cost 2.74777
nbr_neurone :  12  step :  4999 cost 2.69842
nbr_neurone :  13  step :  4998 cost 2.65064
nbr_neurone :  14  step :  4999 cost 2.60828
nbr_neurone :  15  step :  4998 cost 2.56512
nbr_neurone :  16  step :  4998 cost 2.52324
nbr_neurone :  17  step :  4999 cost 2.48304
nbr_neurone :  18  step :  3357 cost 2.44492
nbr_neurone :  19  step :  1541 cost 2.41865
nbr_neurone :  20  step :  1149 cost 2.39046
nbr_neurone :  21  step :  1027 cost 2.37555
nbr_neurone :  22  step :  986 cost 2.35618
nbr_neurone :  23  step :  931 cost 2.34516
nbr_neurone :  24  step :  899 cost 2.32866
nbr_neurone :  25  step :  892 cost 2.32549
nbr_neurone :  26  step :  839 cost 2.31726
nbr_neurone :  27  step :  4997 cost 2.30572
nbr_neurone :  28  step :  4998 cost 2.28985
nbr_neurone :  29  step :  4998 cost 2.27143
nbr_neurone :  30  step :  4999 cost 2.25514
nbr_neurone :  31  step :  4999 cost 2.23839
nbr_neurone :  32  step :  4998 cost 2.22048
nbr_neurone :  33  step :  4998 cost 2.20461
nbr_neurone :  34  step :  4997 cost 2.18591
nbr_neurone :  35  step :  4999 cost 2.17123
nbr_neurone :  36  step :  4998 cost 2.15268
nbr_neurone :  37  step :  4998 cost 2.1389
nbr_neurone :  38  step :  4999 cost 2.12009
nbr_neurone :  39  step :  4999 cost 2.10324
nbr_neurone :  40  step :  4999 cost 2.08588
nbr_neurone :  41  step :  4998 cost 2.06898
nbr_neurone :  42  step :  4999 cost 2.05192
nbr_neurone :  43  step :  4998 cost 2.03623
nbr_neurone :  44  step :  4996 cost 2.0189
nbr_neurone :  45  step :  4999 cost 2.0026
nbr_neurone :  46  step :  4999 cost 1.98593
nbr_neurone :  47  step :  4998 cost 1.96934
nbr_neurone :  48  step :  4997 cost 1.95631
nbr_neurone :  49  step :  4997 cost 1.86931
nbr_neurone :  50  step :  4997 cost 1.80881
nbr_neurone :  51  step :  4999 cost 1.76333
nbr_neurone :  52  step :  4997 cost 1.72412
nbr_neurone :  53  step :  4997 cost 1.68922
nbr_neurone :  54  step :  4998 cost 1.65688
nbr_neurone :  55  step :  4997 cost 1.62625
nbr_neurone :  56  step :  4999 cost 1.5999
nbr_neurone :  57  step :  4996 cost 1.57673
nbr_neurone :  59  step :  4999 cost 1.52258
nbr_neurone :  60  step :  4997 cost 1.5045
nbr_neurone :  61  step :  4996 cost 1.48311

'''