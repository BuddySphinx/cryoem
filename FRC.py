# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 09:05:56 2019

@author: yangq
"""
import numpy as np
import numpy.fft as fft
import matplotlib.pylab as plt
import sys
def spinavg(image):
    #Read the shape and dimension of the input image
    shape=np.shape(image)
    dim=np.size(shape)
    #Record dimensions of the image
    if dim==2:
        nx,ny=shape
        nxdx=np.ceil(nx/2)
        nydy=np.ceil(ny/2)
        x=np.arange(nx)-nxdx + 1
        y=np.arange(ny)-nydy + 1
        [X,Y]=np.meshgrid(x,y)
        index=np.round(np.sqrt(X**2+Y**2))+1
        maxindex=np.max(index)
        output=np.zeros(int(maxindex),dtype=complex)
        sumf=np.zeros(int(maxindex),dtype=complex) 
        count=np.zeros(int(maxindex),dtype=complex)
        for xi in range(nx):
            for yi in range(ny):
                sumf[int(index[xi,yi])-1]=sumf[int(index[xi,yi]-1)-1]+image[xi,yi]
                count[int(index[xi,yi])-1]=count[int(index[xi,yi])-1]+1
        output=sumf/count
        return output
    elif dim==3:
        nx,ny,nz=shape
        nxdx=np.ceil(nx/2)
        nydy=np.ceil(ny/2)
        nzdz=np.ceil(nz/2)
        x=np.arange(nx)-nxdx + 1
        y=np.arange(ny)-nydy + 1
        z=np.arange(nz)-nzdz + 1
        [X,Y,Z]=np.meshgrid(x,y,z)
        index=np.round(np.sqrt(X**2+Y**2+Z**2))+1
        maxindex=np.max(index)
        output=np.zeros(int(maxindex),dtype=complex)
        sumf=np.zeros(int(maxindex),dtype=complex) 
        count=np.zeros(int(maxindex),dtype=complex)
        for xi in range(nx):
            for yi in range(ny):
                for zi in range(nz):
                    sumf[int(index[xi,yi,zi])-1]=sumf[int(index[xi,yi,zi]-1)-1]+image[xi,yi,zi]
                    count[int(index[xi,yi,zi])-1]=count[int(index[xi,yi,zi])-1]+1
        output=sumf/count
        return output
    else:
        print("You need a correct dimension for the input image")
        
def FSC(image1,image2,**kwargs):
    #Calculate fft of the image
    #Separate 2D from 3D
    shape1=np.shape(image1)
    shape2=np.shape(image2)
    if shape1!=shape2:
        print("input image must be square")
        sys.exit(0)
    dim=np.size(shape1)
    if dim==2:
        if shape1[0]!=shape1[1]:
            print("The input image must be a square")
            sys.exit(0)
        else:
            F1=fft.fftshift(fft.fft2(image1))
            F2=fft.fftshift(fft.fft2(image2))
            "F1 and F2 is the structure factor"
            S=spinavg(np.multiply(F1,np.conj(F2)))
            S1=spinavg(np.multiply(F1,np.conj(F1)))
            S2=spinavg(np.multiply(F2,np.conj(F2)))
            FSC_value=np.abs(S)/(np.sqrt(np.abs(np.multiply(S1,S2))))
    if dim==3:
        if shape1[0]!=shape1[1] or shape1[0]!=shape1[2] or shape1[1]!=shape1[2]:
            print("The input image must be a cubic volume")
            sys.exit(0)
        else:
            F1=fft.fftshift(fft.fftn(image1))
            F2=fft.fftshift(fft.fftn(image2))
            "F1 and F2 is the structure factor"
            S=spinavg(np.multiply(F1,np.conj(F2)))
            S1=spinavg(np.multiply(F1,np.conj(F1)))
            S2=spinavg(np.multiply(F2,np.conj(F2)))
            FSC_value=np.abs(S)/(np.sqrt(np.abs(np.multiply(S1,S2))))
    return FSC_value
#This is the test batch
SNRt=0.1
r=np.arange(1+np.shape(class1)[0]/2)
n=a*np.pi*r
n[0]=1
eps=np.finfo(float).eps
t1=np.divide(np.ones(np.shape(n)),n+eps)
t2=SNRt
