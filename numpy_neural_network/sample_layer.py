
import numpy as np
import numpy_neural_network as npnn
from numpy_neural_network import Layer

class Sample(Layer):
    '''variational autoencoder (VAE) sample layer'''

    def __init__(self, shape_out):

        shape_in = (shape_out[0], shape_out[1], 2 * shape_out[2])

        super(Sample, self).__init__(shape_in, shape_out, None)

        self.x_mean = None
        self.x_variance = None

        self.train_z = None  # training mode hidden state z vector

    def forward(self, x):

        self.x_variance = x[:,:,:self.shape_out[2]]
        self.x_mean     = x[:,:,self.shape_out[2]:]

        if self.is_training:
            # the mean of gausian sampled variance mean(x_mean + N(0, I)) is 0, which
            # means that x_mean represents the mean vector of the distribution
            self.y = self.x_mean + self.x_variance * np.random.normal(0.0, 1.0, self.x_variance.shape)

            if self.train_z is not None:
                self.train_z.append(self.y)  # collect hidden state z data for evaluation
        else:
            # non-training mode z = hidden state mean (its the expected value) ...
            self.y = self.x_mean

        return self.y

    def backward(self, grad_y):

        # KL mean gradient = derivative of: 0.5*(x_mean^2) ...
        kl_mean_grad = self.x_mean

        # KL variance gradient = derivative of: 0.5*(x_variance - log(variance) - 1) ...
        kl_variance_grad = 0.5 - np.divide(0.5, self.x_variance + 1e-9)

        # combine the gradients from the decoder with the KL gradients ...
        grad_y_mean     = grad_y + kl_mean_grad
        grad_y_variance = grad_y + kl_variance_grad

        self.grad_x[:,:,:self.shape_out[2]] = grad_y_variance
        self.grad_x[:,:,self.shape_out[2]:] = grad_y_mean

        return self.grad_x

    def step_init(self, is_training=False):
        '''
        this method may initialize some layer internals before each optimizer mini-batch step
        '''
        self.is_training = is_training

        if is_training and self.train_z is not None:
            self.train_z = []


