"""
This is the NeuralNetwork class
"""

import torch
from torch import nn
import numpy as np
import yaml
from torchsummary import summary


class Net(nn.Module):

    def __init__(self):
        super(Net, self).__init__()

        # loads hyperparameters.yaml into a dict
        with open('hyperparameters.yaml') as f:
            hp = yaml.safe_load(f)['hyperparameters']

        # loads hyperparameters into individual variables
        channels, height, width = hp['input_shape']
        out_1, kernel_1, stride_1, padding_1 = hp['conv_1']
        out_2, kernel_2, stride_2, padding_2 = hp['conv_2']
        out_3, kernel_3, stride_3, padding_3 = hp['conv_3']
        out_4, kernel_4, stride_4, padding_4 = hp['conv_4']
        out_5, kernel_5, stride_5, padding_5 = hp['conv_5']
        out_6, kernel_6, stride_6, padding_6 = hp['conv_6']
        self.out_7, kernel_7, stride_7, padding_7 = hp['conv_7']

        # features block - consists of convolutional layers and extracts key features
        self.features = nn.Sequential(
            # input layer
            nn.Conv2d(channels, out_1, kernel_size=kernel_1, stride=stride_1, padding=padding_1, bias=False)

            # depthwise convolution layer 1
            , nn.Conv2d(out_1, out_1, kernel_size=kernel_2, stride=stride_2, padding=padding_2, groups=out_1, bias=False)
            , nn.BatchNorm2d(out_1)
            , nn.ReLU(inplace=True)
            , nn.Conv2d(out_1, out_2, 1, 1, 0, bias=False)
            , nn.BatchNorm2d(out_2)
            , nn.ReLU(inplace=True)

            # depthwise convolution layer 2
            , nn.Conv2d(out_2, out_2, kernel_size=kernel_3, stride=stride_3, padding=padding_3, groups=out_2, bias=False)
            , nn.BatchNorm2d(out_2)
            , nn.ReLU(inplace=True)
            , nn.Conv2d(out_2, out_3, 1, 1, 0, bias=False)
            , nn.BatchNorm2d(out_3)
            , nn.ReLU(inplace=True)

            # depthwise convolution layer 3
            , nn.Conv2d(out_3, out_3, kernel_size=kernel_4, stride=stride_4, padding=padding_4, groups=out_3, bias=False)
            , nn.BatchNorm2d(out_3)
            , nn.ReLU(inplace=True)
            , nn.Conv2d(out_3, out_4, 1, 1, 0, bias=False)
            , nn.BatchNorm2d(out_4)
            , nn.ReLU(inplace=True)

            # depthwise convolution layer 4
            , nn.Conv2d(out_4, out_4, kernel_size=kernel_5, stride=stride_5, padding=padding_5, groups=out_4, bias=False)
            , nn.BatchNorm2d(out_4)
            , nn.ReLU(inplace=True)
            , nn.Conv2d(out_4, out_5, 1, 1, 0, bias=False)
            , nn.BatchNorm2d(out_5)
            , nn.ReLU(inplace=True)

            # depthwise convolution layer 5
            , nn.Conv2d(out_5, out_5, kernel_size=kernel_6, stride=stride_6, padding=padding_6, groups=out_5, bias=False)
            , nn.BatchNorm2d(out_5)
            , nn.ReLU(inplace=True)
            , nn.Conv2d(out_5, out_6, 1, 1, 0, bias=False)
            , nn.BatchNorm2d(out_6)
            , nn.ReLU(inplace=True)

            # depthwise convolution layer 6
            , nn.Conv2d(out_6, out_6, kernel_size=kernel_7, stride=stride_7, padding=padding_7, groups=out_6, bias=False)
            , nn.BatchNorm2d(out_6)
            , nn.ReLU(inplace=True)
            , nn.Conv2d(out_6, self.out_7, 1, 1, 0, bias=False)
            , nn.BatchNorm2d(self.out_7)
            , nn.ReLU(inplace=True)

            , nn.AvgPool2d(7)
        )

        # classifier block - consists of linear layer that converges to two classes
        self.classifier = nn.Sequential(
            nn.Linear(self.out_7 * 16, 2)
        )

    '''
    calculates size of convolution layer outputs
    
    :param h: height of input image
    :param w: width of input image
    :param conv: the convolution layer
    :param pool: size of pooling layer
    '''
    @classmethod
    def get_conv_size(h, w, conv: nn.Conv2d, pool=1):
        size = conv.kernel_size
        stride = conv.stride
        padding = conv.padding
        dilation = conv.dilation

        # calculates the size of the convolution layer
        h = np.floor((h + 2 * padding[0] - dilation[0] * (size[0] - 1) - 1) / stride[0] + 1) / pool
        w = np.floor((w + 2 * padding[1] - dilation[1] * (size[1] - 1) - 1) / stride[1] + 1) / pool

        return int(h), int(w)


    '''
    neural network's forward propagation method
    
    :param x: the input tensor that will be propagated throughout the network
    '''
    @staticmethod
    def forward(self, x):
        x = self.features(x)                # runs tensor through the features block
        x = x.view(-1, self.out_7 * 16)     # flattens tensor
        x = self.classifier(x)              # runs tensor through the classifier block
        return x                            # returns the network's output


if __name__ == '__main__':
    net = Net().cuda()
    print(summary(net, input_size=(3, 224, 224)))
