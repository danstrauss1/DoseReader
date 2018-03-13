import pydicom, numpy as np
import matplotlib.pyplot as plt


dose = pydicom.read_file(r'C:\Users\User\Documents\DoseVolumeTest\DoseVolumeTest.dcm')


# Build x, y, z, position grids
xgrid = np.arange(dose.ImagePositionPatient[0], dose.Rows, dose.PixelSpacing[0])
ygrid = np.arange(dose.ImagePositionPatient[1], dose.Columns, dose.PixelSpacing[1])
zgrid = np.arange(dose.ImagePositionPatient[2], dose.NumberOfFrames, int(dose.GridFrameOffsetVector[1-0]))



planes, rows, cols = dose.NumberOfFrames, dose.Columns, dose.Rows
image = dose.pixel_array # should have shape (planes, rows, cols)

# to get data and coords to write to CSV
image_data = image.ravel()
z, y, x = np.meshgrid(np.arange(planes), np.arange(rows), np.arange(cols),
                      indexing='ij')



# Compute gradient matrix
grad = np.gradient(dose.pixel_array)

# Compute norm of grad matrix
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
index = np.where(dose.pixel_array > mindose)

xindex = index[0]
yindex = index[1]
zindex = index[2]


points = []

# Create a list of points (x, y, z, Dose, Gradient)
for i in range(len(index[0])):
    points.append([xgrid[xindex[i]], ygrid[yindex[i]], zgrid[zindex[i]],
                   dose.DoseGridScaling * 100 * dose.pixel_array[xindex[i]][yindex[i]][zindex[i]],
                   gradnorm[xindex[i]][yindex[i]][zindex[i]]])


# Sort points list by gradient:
sortedpoints = sorted(points, key=lambda x: x[4])

def printpoints(numOfPoints):

    for i in range(numOfPoints):
        print("({:.4}, {:.4}, {:.4}) : {:.4} cGy Gradient = {}".format(
            sortedpoints[i][0] / 10,
            (sortedpoints[i][1] + np.max(ygrid)) / 10,
            sortedpoints[i][2] / 10,
            sortedpoints[i][3],
            sortedpoints[i][4]
        ))