import pydicom, numpy as np

dose = pydicom.read_file('DoseVolumeTest.dcm')
d = np.fromstring(dose.PixelData, dtype=np.int16)
#d = d.reshape((dose.NumberOfFrames, dose.Columns, dose.Rows))


# Build x, y, z, position grids
xgrid = np.arange(dose.ImagePositionPatient[0], dose.Columns, dose.PixelSpacing[0])
ygrid = np.arange(dose.ImagePositionPatient[1], dose.Rows, dose.PixelSpacing[1])
zgrid = np.arange(dose.ImagePositionPatient[2], dose.NumberOfFrames, int(dose.GridFrameOffsetVector[1-0]))


# Reshape 1D arrays to 3D Cubes for both x,y,z axis
# Determine how to index like MATLAB does
xcube = np.stack(xgrid)
ycube = np.stack(ygrid)
zcube = np.stack(zgrid)

# Compute gradient matrix
grad = np.gradient(d)


# minimum dose in Gy

dosethreshold = 0.5
mindose = dosethreshold * np.max(dose.pixel_array * dose.DoseGridScaling)

# Find indicies which satsify dosethreshold requirements
index = np.argwhere(d > mindose)

