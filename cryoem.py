# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 21:55:54 2019

@author: yangq
"""

#This is a test file for cryo em data handling
import mrcfile 
import numpy as np
import matplotlib.pylab as plt
mrc=mrcfile.mmap('test.mrc',mode='r+',permissive=True)
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
from numpy import fft
class_mrc=mrcfile.mmap('class_averages.mrcs',mode='r+',permissive=True) 
class1=class_mrc.data[0,:,:]
class2=class_mrc.data[1,:,:]
r,c=np.shape(class1)
class_slice=class1[:,1]
def LSQ_1D(xs,ys,mu,sigma,pi,maxiter,tol=0.001):
    num=len(xs)
    Jacob=np.zeros([num,3])
    def gaussian(mu,sigma,pi,xs):
        ys=np.array([pi*np.exp(-(xs-mu)**2/(2*sigma**2))])
        return ys
    for iteration in range(1,maxiter):
        d_beta=ys-gaussian(mu,sigma,pi,xs)
        Jacob=np.array([gaussian(mu,sigma,pi,xs)/pi,gaussian(mu,sigma,pi,xs)*(xs-mu)/(sigma**2),gaussian(mu,sigma,pi,xs)*(xs-mu)**2/(-sigma**3)])
        Jacob=np.reshape(Jacob,(3,num))
        d_lambda=np.linalg.solve(np.matmul(Jacob,np.transpose(Jacob)),np.matmul(Jacob,np.transpose(d_beta)))
        if d_lambda<tol:
            print("The iteration has converged at {}".format(iteration))
            break
        else:
            pi,mu,sigma=d_lambda+np.array(pi,mu,sigma)
    return pi,mu,sigma
        
        
        
        
    
    #return ws
    
            
    
    
