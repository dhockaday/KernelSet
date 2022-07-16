import math
import random
import torch
import torch.nn as nn
from termcolor import colored,cprint
import math
import  arguments



def get_gaussian_filter(epoch_number,mean =1, kernel_size=3, sigma=2, channels=3):
    # Create a x, y coordinate grid of shape (kernel_size, kernel_size, 2)
    parameter = arguments.get_args()

    kernel_number = parameter.kernel_type
    #filter_list = ['topLeft', 'topRight', 'bottomLeft', 'bottomRight']
    if kernel_number == 1:
        filter_list = ['topLeft', 'bottomRight']
        print ("Kernel Type 1: top-left, bottom-right")

    elif kernel_number == 2:
        filter_list = ['bottomLeft', 'topRight']
        print("Kernel Type 2: bottom-left, top-right")

    elif kernel_number == 3:
        filter_list = ['topLeft', 'bottomLeft']
        print ("Kernel Type 3: top-left, bottom-left")

    elif kernel_number == 4:
        filter_list = ['topRight', 'bottomRight']
        print ("kernel Type 4: top-right, bottom-right")
    elif kernel_number == 5:
        filter_list = ['topLeft', 'topRight']
        print ("Kernel Type 5: top-left, top-right")
    elif kernel_number == 6:
        filter_list = ['bottomLeft', 'bottomRight']
        print ("Kernel Type 6: bottom-left, bottom-right")





    if math.isnan(mean) or math.isnan(sigma):
        mean = 1
        sigma = 1

    '''
    kernel_type Description
    
    1 = top left bottom right
    2 = bottom left top right
    
    3 = top left bottom left
    4 = top right bottom right
    
    5 = top left top right
    6 = bottom left bottom right
    '''


     #Exp 2 , 3 and 4 Kernel

    #filter_list = ['topLeft', 'bottomRight'] #Exp 2
    #filter_list = ['topLeft', 'forceG'] #Exp 3
    #filter_list = ['bottomRight', 'forceG'] #Exp 4


    #filter_list = ['topLeft'] #Exp 5
    #filter_list = ['bottomRight'] #Exp 6
    #filter_list = ['forceG']  # Exp 7

    #filter_list = ['topLeft', 'topRight', 'bottomLeft', 'bottomRight', 'middle-left', 'middle-right', 'middle-top', 'middle-bottom']  # Exp 8

    #filter_name = filter_list[random.randint(0, 4)] # Exp 1
    filter_name = filter_list[random.randint(0, 1)] # Exp 2 Kernel Set
    #filter_name = filter_list[0] # Exp 5~7
    #filter_name = filter_list[random.randint(0, 3)] #Exp 4 Kernel
    #filter_name = filter_list[random.randint(0, 7)] # Exp 8 kernel


    x_coord = torch.arange(kernel_size)
    x_grid = x_coord.repeat(kernel_size).view(kernel_size, kernel_size)
    y_grid = x_grid.t()
    xy_grid = torch.stack([x_grid, y_grid], dim=-1).float()

    if filter_name == 'forceG':
        mean = 1
        sigma = 1
    else:
        mean = mean
        sigma = sigma

    variance = sigma**2.

    cprint("Sigma: " + str(sigma) + " --Variance: " + str(variance) + " --mean: " + str(mean), "red", "on_white")

    # Calculate the 2-dimensional gaussian kernel which is
    # the product of two gaussian distributions for two different
    # variables (in this case called x and y)
    gaussian_kernel = (1./(2.*math.pi*variance)) *\
                      torch.exp(
                          -torch.sum((xy_grid - mean)**2., dim=-1) /\
                          (2*variance)
                      )

    # Make sure sum of values in gaussian kernel equals 1.
    gaussian_kernel = gaussian_kernel / torch.sum(gaussian_kernel)


    if filter_name == 'topLeft':
        cprint("Top Left", "red", "on_white")
        print(gaussian_kernel)

    elif filter_name == 'bottomRight':
        temp = gaussian_kernel[0].clone()
        gaussian_kernel[0] = gaussian_kernel[2]
        gaussian_kernel[2] = temp
        idx = torch.LongTensor([2, 1, 0])
        gaussian_kernel = torch.index_select(gaussian_kernel, 1, idx)
        cprint("Bottom Right", "red", "on_white")
        print(gaussian_kernel)

    elif filter_name == 'topRight':
        idx = torch.LongTensor([2, 1, 0])
        gaussian_kernel = torch.index_select(gaussian_kernel, 1, idx)
        cprint("Top Right", "red", "on_white")
        print(gaussian_kernel)

    elif filter_name == 'bottomLeft':
        idx = torch.LongTensor([2, 1, 0])
        gaussian_kernel = torch.index_select(gaussian_kernel, 0, idx)
        cprint("Bottom Left", "red", "on_white")
        print(gaussian_kernel)

    elif filter_name == 'middle-left':
        temp = gaussian_kernel.clone()
        gaussian_kernel[1][0] = temp[0][0]
        gaussian_kernel[1][1] = temp[1][1]
        gaussian_kernel[1][2] = temp[2][2]

        gaussian_kernel[0][0] = temp[0][1]
        gaussian_kernel[2][0] = temp[0][1]

        gaussian_kernel[0][1] = temp[0][2]
        gaussian_kernel[2][1] = temp[0][2]

        gaussian_kernel[0][2] = temp[1][2]
        gaussian_kernel[2][2] = temp[1][2]

        cprint("middle left", "red","on_white")
        print(gaussian_kernel)

    elif filter_name == 'middle-right':
        temp = gaussian_kernel.clone()
        gaussian_kernel[1][2] = temp[0][0]
        gaussian_kernel[1][1] = temp[1][1]
        gaussian_kernel[1][0] = temp[2][2]

        gaussian_kernel[0][2] = temp[0][1]
        gaussian_kernel[2][2] = temp[0][1]

        gaussian_kernel[0][1] = temp[0][2]
        gaussian_kernel[2][1] = temp[0][2]

        gaussian_kernel[0][0] = temp[1][2]
        gaussian_kernel[2][0] = temp[1][2]

        cprint("middle right", "red", "on_white")
        print(gaussian_kernel)

    elif filter_name == 'middle-top':
        temp = gaussian_kernel.clone()
        gaussian_kernel[0][1] = temp[0][0]
        gaussian_kernel[1][1] = temp[1][1]
        gaussian_kernel[2][1] = temp[2][2]

        gaussian_kernel[0][0] = temp[0][1]
        gaussian_kernel[0][2] = temp[0][1]

        gaussian_kernel[1][0] = temp[0][2]
        gaussian_kernel[1][2] = temp[0][2]

        gaussian_kernel[2][0] = temp[1][2]
        gaussian_kernel[2][2] = temp[1][2]

        cprint("middle top", "red", "on_white")
        print(gaussian_kernel)


    elif filter_name == 'middle-bottom':
        temp = gaussian_kernel.clone()
        gaussian_kernel[2][1] = temp[0][0]
        gaussian_kernel[1][1] = temp[1][1]
        gaussian_kernel[0][1] = temp[2][2]

        gaussian_kernel[2][0] = temp[0][1]
        gaussian_kernel[2][2] = temp[0][1]

        gaussian_kernel[1][0] = temp[0][2]
        gaussian_kernel[1][2] = temp[0][2]

        gaussian_kernel[0][0] = temp[1][2]
        gaussian_kernel[0][2] = temp[1][2]

        cprint("middle bottom", "red", "on_white")
        print(gaussian_kernel)








    # Reshape to 2d depthwise convolutional weight
    gaussian_kernel = gaussian_kernel.view(1, 1, kernel_size, kernel_size)
    gaussian_kernel = gaussian_kernel.repeat(channels, 1, 1, 1)
    if kernel_size == 3:
        padding = 1
    elif kernel_size == 5:
        padding = 2
    else:
        padding = 0

    gaussian_filter = nn.Conv2d(in_channels=channels, out_channels=channels,
                                kernel_size=kernel_size, groups=channels,
                                bias=False, padding=padding)

    gaussian_filter.weight.data = gaussian_kernel
    gaussian_filter.weight.requires_grad = False
    
    return gaussian_filter
