import numpy as np
import matplotlib.pyplot as plt
import functions
import tensorflow as tf
import plot


def sgd(parameters, func_name, iterations, lr):
    filenames = []
    loss = []

    opt = tf.keras.optimizers.SGD(learning_rate=lr)
    var1 = tf.Variable(-2.)
    var2 = tf.Variable(-4.)
    func = None
    #
    if func_name == 'rosenbrock':
        def cost(): return ((parameters[0] - var1)
                            ** 2) + parameters[1]*((var1-(var2**2))**2)
        func = functions.rosenbrock
    elif func_name == 'rastrigin':
        def cost(): return (var1**2 - parameters * np.cos(2*np.pi * var1)) + \
            (var2**2 - parameters * np.cos(2*np.pi * var2))
        func = functions.rastrigin()
    # First step is `- learning_rate * grad`

    for i in range(iterations):
        opt.minimize(cost, [var1, var2]).numpy()
        loss.append(cost().numpy())
        print('Loss: ', cost().numpy())
        print('x: ', var1.numpy())
        print('y: ', var2.numpy())
        filenames.append(plot.plotGraphs_sgd(
            [var1.numpy(), var2.numpy()], func, parameters, i))

    plot.createGif(filenames, name="sgd_gif.gif")

    plot.plotLoss([loss,list(range(0, 100))], name = "Loss_sgd.png")
    #plt.plot(loss)
    #plt.title("SGD Loss")
    #plt.xlabel('Epochs')
    #plt.ylabel('Loss')
    #plt.show()
