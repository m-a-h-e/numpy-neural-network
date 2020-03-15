#!/usr/bin/env python

import sys
sys.path.append("../../")

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import numpy_neural_network as npnn
import npnn_datasets

matplotlib.rcParams['toolbar'] = 'None'

################################################################################

model = npnn.network.Model([
    npnn.Conv2d(shape_in=(10, 10, 1), shape_out=(8, 8, 8), kernel_size=3, stride=1),
    npnn.LeakyReLU(8*8*8),
    npnn.MaxPool(shape_in=(8, 8, 8), shape_out=(4, 4, 8), kernel_size=2),
    npnn.Conv2d(shape_in=(4, 4, 8), shape_out=(2, 2, 6), kernel_size=3, stride=1),
    npnn.LeakyReLU(2*2*6),
    npnn.MaxPool(shape_in=(2, 2, 6), shape_out=(1, 1, 6), kernel_size=2),
    npnn.FullyConn(6, 4),
    npnn.Softmax(4)
])

model.loss_layer = npnn.loss_layer.CrossEntropyLoss(4)

optimizer = npnn.optimizer.Adam(model, alpha=1e-2)

optimizer.dataset = npnn_datasets.FourImgClasses()

################################################################################

plt.ion()
plt.show()
fig1, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(10,8))

fig2, ((ax1b, ax2b), (ax3b, ax4b)) = plt.subplots(2, 2, figsize=(10,8))

episodes = []

mini_train_loss = []
mini_validation_loss = []
mini_train_accuracy = []
mini_validation_accuracy = []

train_loss = []
valid_loss = []
train_accuracy = []
valid_accuracy = []

for episode in np.arange(1000):

    # step the optimizer ...
    optimizer.step()
    episodes.append(episode)

    #===========================================================================
    # mini batch loss and accuracy
    #===========================================================================

    mini_train_loss.append(np.mean(optimizer.loss))
    mini_train_accuracy.append(optimizer.accuracy * 100.0)

    ax1.cla()
    ax1.set_xlabel('episode')
    ax1.set_ylabel('train mini-batch loss')
    ax1.set_yscale('log')
    ax1.set_ylim((min(mini_train_loss)/2.0, max(mini_train_loss)*2.0))
    ax1.plot(episodes, mini_train_loss)

    ax2.cla()
    ax2.set_xlabel('episode')
    ax2.set_ylabel('train mini-batch accuracy')
    ax2.set_ylim(-10, 110)
    ax2.plot(episodes, mini_train_accuracy)

    #===========================================================================
    # complete dataset loss and accuracy
    #===========================================================================

    tloss, taccuracy = optimizer.calculate_loss(optimizer.dataset.x_train_data, optimizer.dataset.y_train_data)
    train_loss.append(np.mean(tloss))
    train_accuracy.append(taccuracy * 100.0)

    vloss, vaccuracy = optimizer.calculate_loss(optimizer.dataset.x_validation_data, optimizer.dataset.y_validation_data)
    valid_loss.append(np.mean(vloss))
    valid_accuracy.append(vaccuracy * 100.0)

    # print the episode and loss values ...
    print("episode = {0:5d}, tloss = {1:8.6f}, vloss = {2:8.6f}, taccuracy = {3:8.6f}, vaccuracy = {3:8.6f}".format(
        episode, np.mean(tloss), np.mean(vloss), taccuracy * 100.0, vaccuracy * 100.0
    ))

    ax3.cla()
    ax3.set_xlabel('episode')
    ax3.set_ylabel('dataset loss')
    ax3.set_yscale('log')
    ax3.set_ylim((min(min(train_loss), min(valid_loss))/2.0, max(max(train_loss), max(valid_loss))*2.0))
    ax3.plot(episodes, train_loss, episodes, valid_loss)

    ax4.cla()
    ax4.set_xlabel('episode')
    ax4.set_ylabel('dataset accuracy')
    ax4.set_ylim(-10, 110)
    ax4.plot(episodes, train_accuracy, episodes, valid_accuracy)

    #===========================================================================
    # batch network output plots
    #===========================================================================

    k = np.arange(optimizer.train_x_batch.shape[0])

    ax1b.cla()
    ax1b.set_ylabel('mini-batch class 0')
    ax1b.set_ylim(-0.1, 1.1)
    ax1b.scatter(k, optimizer.train_t_batch[:,0], s=10, c='tab:green')
    ax1b.scatter(k, optimizer.train_y_batch[:,0], s=10, c='tab:orange')

    ax2b.cla()
    ax2b.set_ylabel('mini-batch class 1')
    ax2b.set_ylim(-0.1, 1.1)
    ax2b.scatter(k, optimizer.train_t_batch[:,1], s=10, c='tab:green')
    ax2b.scatter(k, optimizer.train_y_batch[:,1], s=10, c='tab:orange')

    ax3b.cla()
    ax3b.set_ylabel('mini-batch class 2')
    ax3b.set_ylim(-0.1, 1.1)
    ax3b.scatter(k, optimizer.train_t_batch[:,2], s=10, c='tab:green')
    ax3b.scatter(k, optimizer.train_y_batch[:,2], s=10, c='tab:orange')

    ax4b.cla()
    ax4b.set_ylabel('mini-batch class 3')
    ax4b.set_ylim(-0.1, 1.1)
    ax4b.scatter(k, optimizer.train_t_batch[:,3], s=10, c='tab:green')
    ax4b.scatter(k, optimizer.train_y_batch[:,3], s=10, c='tab:orange')

    #===========================================================================
    # draw and save PNG to generate video files later on
    #===========================================================================

    plt.draw()
    fig1.savefig('png1/episode{0:04d}.png'.format(episode))
    fig2.savefig('png2/episode{0:04d}.png'.format(episode))
    plt.pause(0.001)

input("Press Enter to close ...")

