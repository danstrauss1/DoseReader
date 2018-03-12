import numpy as np
import pydicom
import matplotlib

file = r"C:\Users\User\Documents\DoseVolumeTest\DoseVolumeTest.dcm"

ds = pydicom.dcmread(file)


# Find grid spacing and resolution
xstart, ystart, zstart = ds.ImagePositionPatient
xstep, ystep = ds.PixelSpacing
xres, yres = ds.Rows, ds.Columns

# Compute Gradient:
gradmatrix = np.gradient(ds.pixel_array)

maxdose = np.max(ds.pixel_array * ds.DoseGridScaling)

dosethreshold = 0.5 * maxdose #Dose Theshold in Gy

xindex, yindex, zindex = np.where(ds.pixel_array >= dosethreshold)

xgrid = np.mgrid[xstart:]

print("Max Dose is : {} {}".format(maxdose, ds.DoseUnits))
print("The Dose Theshold is : {} {}".format(dosethreshold, ds.DoseUnits))
print("Index of points : ({}, {}, {})".format(xindex, yindex, zindex))


xgrad = gradmatrix[xindex, :, :]
ygrad = gradmatrix[:, yindex, :]
zgrad = gradmatrix[:, :, zindex]