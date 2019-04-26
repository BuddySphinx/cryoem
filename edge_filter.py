# -*- coding: utf-8 -*-
"""
Created on Mon Feb 11 22:26:58 2019

@author: yangq
"""

#Sobel filter
import numpy as np
import matplotlib.pyplot as plt 
image=plt.imread("height.tif")
kernel_x=np.mat('-1 0 1;-2 0 2;-1 0 1')
kernel_y=np.mat('-1 -2 -1;0 0 0;1 2 1')
#image_R=image[:,:,0]
#image_G=image[:,:,1]
#image_B=image[:,:,2]
#class operator(object):
def rgb2gray(image):
    r,g,b=image[:,:,0],image[:,:,1],image[:,:,2]
    gray=0.2989*r+0.5870*g+0.1140*b
    return gray
def Sobel_full(kernel_x,kernel_y,image):
    image_new=np.zeros(np.shape(image))
    for x in range(1,int(np.shape(image)[0])-1):
        for y in range(1,int(np.shape(image)[1])-1):
            pixel_x=kernel_x[0,0]*image[x-1,y-1]+kernel_x[1,0]*image[x,y-1]+kernel_x[2,0]*image[x+1,y-1]+kernel_x[0,1]*image[x-1,y]+kernel_x[1,1]*image[x,y]+kernel_x[2,1]*image[x+1,y]+kernel_x[0,2]*image[x-1,y+1]+kernel_x[1,2]*image[x,y+1]+kernel_x[2,2]*image[x+1,y+1]
            pixel_y=kernel_y[0,0]*image[x-1,y-1]+kernel_y[1,0]*image[x,y-1]+kernel_y[2,0]*image[x+1,y-1]+kernel_y[0,1]*image[x-1,y]+kernel_y[1,1]*image[x,y]+kernel_y[2,1]*image[x+1,y]+kernel_y[0,2]*image[x-1,y+1]+kernel_y[1,2]*image[x,y+1]+kernel_y[2,2]*image[x+1,y+1]
            pixel=np.sqrt(pixel_x**2+pixel_y**2)
            image_new[x,y]=pixel
    return image_new
def Sobel_x(kernel_x,image):
    image_new=np.zeros(np.shape(image))
    for x in range(1,int(np.shape(image)[0])-1):
        for y in range(1,int(np.shape(image)[1])-1):
            pixel_x=kernel_x[0,0]*image[x-1,y-1]+kernel_x[1,0]*image[x,y-1]+kernel_x[2,0]*image[x+1,y-1]+kernel_x[0,1]*image[x-1,y]+kernel_x[1,1]*image[x,y]+kernel_x[2,1]*image[x+1,y]+kernel_x[0,2]*image[x-1,y+1]+kernel_x[1,2]*image[x,y+1]+kernel_x[2,2]*image[x+1,y+1]
            image_new[x,y]=pixel_x
    return image_new
def Sobel_y(kernel_y,image):
    image_new=np.zeros(np.shape(image))
    for x in range(1,int(np.shape(image)[0])-1):
        for y in range(1,int(np.shape(image)[1])-1):
            pixel_y=kernel_y[0,0]*image[x-1,y-1]+kernel_y[1,0]*image[x,y-1]+kernel_y[2,0]*image[x+1,y-1]+kernel_y[0,1]*image[x-1,y]+kernel_y[1,1]*image[x,y]+kernel_y[2,1]*image[x+1,y]+kernel_y[0,2]*image[x-1,y+1]+kernel_y[1,2]*image[x,y+1]+kernel_y[2,2]*image[x+1,y+1]
            image_new[x,y]=pixel_y
    return image_new
def normalization(image,*kernel):
    newimage=np.zeros(image.shape)
    max_I=np.max(image)
    min_I=np.min(image)
    if 'linear' in kernel:
        newimage=(image-min_I)/(max_I-min_I)
        return newimage
    elif 'sigmoid' in kernel:
        for idx in np.ndindex(image.shape):
            pixel=image[idx]
            newimage[idx]=1/(1+np.exp(-2*pixel))
        return newimage
    elif 'gaussian' in kernel:
        newimage=(image-np.mean(image))/np.std(image)
        return newimage
    else:
        print('please specify a kernel')
Noise=np.random.normal(0,1,size=np.shape(image_R))
def mask_image(image,mask_radius):
    r,c=np.shape(image)
    newimage=np.zeros(image.shape)
    if 2*mask_radius>np.min([r,c]):
        print("pick a smaller radius, smaller than {}".format(np.min([r,c])/2))
    else:
        center=np.array([r/2,c/2])
        for idx in np.ndindex(image.shape):
            idx_temp=np.asarray(idx)
            dis=np.sqrt((idx_temp-center)[0]**2+(idx_temp-center)[1]**2)
            if dis<mask_radius:
                newimage[idx]=image[idx]
            else:
                newimage[idx]=0
        return newimage
#from numpy import fft 
#image_fft=fft.fft2(image_R)
#image_fft_phase=image_fft/np.abs(image_fft)
#image_fft_newphase=image_fft_phase*np.exp(1j*0.5*np.pi)
#image_fft_new=image_fft_newphase*np.abs(image_fft)
#Image_new_phase=fft.ifft2(image_fft_new)



