

import numpy as np
import pydicom
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import plotly.plotly as py
import plotly.graph_objs as go
import pandas as pd

file = r'C:\Users\User\Documents\DoseVolumeTest\DoseVolumeTest.dcm'

dicom = pydicom.dcmread(file)

slice = dicom.pixel_array[100]

#plt.imshow(dicom.pixel_array[100])






def plotslices():
    for i in range(3):
        for j in range(3):
            for k in range(3):

                if i == j or i ==k or j ==k:
                    pass

                else:

                    view = np.transpose(dicom.pixel_array, (i, j, k))
                    plt.figure(i)
                    plt.imshow(view[100])
                    plt.title("View {}, {}, {}".format(i, j, k))



'''
xsize = np.shape(slice)[0]
ysize = np.shape(slice)[1]
zsize = 100

x = np.linspace(0, xsize, xsize)
y = np.linspace(0, ysize, ysize)
z = np.linspace(0, zsize, zsize)
X, Y = np.meshgrid(x, y)

grad = np.gradient(dicom.pixel_array)
grad = np.sqrt((grad[0])**2 + (grad[1])**2 + (grad[2])**2)

print('done')

'''