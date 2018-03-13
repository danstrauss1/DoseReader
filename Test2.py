import pydicom, numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

dose = pydicom.read_file(r'C:\Users\User\Documents\DoseVolumeTest\DoseVolumeTest.dcm')
#d = np.fromstring(dose.PixelData, dtype=np.int16)
#d = d.reshape((dose.NumberOfFrames, dose.Columns, dose.Rows))


# Build x, y, z, position grids
xgrid = np.arange(dose.ImagePositionPatient[0], dose.Rows, dose.PixelSpacing[0])
ygrid = np.arange(dose.ImagePositionPatient[1], dose.Columns, dose.PixelSpacing[1])
zgrid = np.arange(dose.ImagePositionPatient[2], dose.NumberOfFrames, int(dose.GridFrameOffsetVector[1-0]))


# Reshape 1D arrays to 3D Cubes for both x,y,z axis
# Determine how to index like MATLAB does
xcube = np.stack((xgrid, xgrid, xgrid))
ycube = np.stack((ygrid, ygrid, ygrid))
zcube = np.stack((zgrid, zgrid, zgrid))

# Compute gradient matrix
grad = np.gradient(dose.pixel_array)

gradnorm = np.sqrt(grad[0]**2 + grad[1]**2 + grad[2]**2)

def printDoseGradient(level):
    gradlevel = gradnorm[level]
    doselevel = dose.pixel_array[level]

    plt.imshow(doselevel)
    plt.quiver(grad[0][100], grad[1][100], grad[2][100])


# minimum dose in Gy

dosethreshold = 0.5
maxdose = np.max(dose.pixel_array)
mindose = dosethreshold * maxdose

# Find indicies which satsify dosethreshold requirements
#index = np.argwhere(dose.pixel_array > mindose)
#index = np.nonzero(dose.pixel_array > mindose)
index = np.where(dose.pixel_array > mindose)

xindex = index[0]
yindex = index[1]
zindex = index[2]

'''
mingrad = 100
gradindex = np.nonzero(gradnorm < mingrad)

xgrad = gradindex[0]
ygrad = gradindex[1]
zgrad = gradindex[2]
'''

# Dose at point 0

print(dose.DoseGridScaling * dose.pixel_array[xindex[0]][yindex[0]][zindex[0]])

# Gradient at point 0
print(gradnorm[xindex[0]][yindex[0]][zindex[0]])

points = []

# Create a list of points (x, y, z, Dose, Gradient)
for i in range(len(index[0])):
    points.append([xindex[i], yindex[i], zindex[i],
                   dose.DoseGridScaling * 100 * dose.pixel_array[xindex[i]][yindex[i]][zindex[i]],
                   gradnorm[xindex[i]][yindex[i]][zindex[i]]])


# Sort points list by gradient:
sortedpoints = sorted(points, key=lambda x: x[4])

def printpoints(numOfPoints):
    #for i in range(numOfPoints):
        #print("Point {} : ({}, {}, {}) - Dose: {:.4} cGy".format(i+1, xindex[i], yindex[i], zindex[i], 100 * dose.DoseGridScaling * dose.pixel_array[xindex[i]][yindex[i]][zindex[i]]))

    for i in range(numOfPoints):
        #print(sortedpoints[i])
        print("({}, {}, {}) : {:.4} cGy Gradient = {:.4}".format(
            sortedpoints[i][0],
            sortedpoints[i][1],
            sortedpoints[i][2],
            sortedpoints[i][3],
            sortedpoints[i][4]
        ))