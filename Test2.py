import pydicom, numpy as np
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import filedialog, ttk

def dosegradient(fname, numOfPoints, threshold):

    #dose = pydicom.read_file(r'C:\Users\User\Documents\DoseVolumeTest\DoseVolumeTest.dcm')
    dose = pydicom.read_file(fname)

    # Build x, y, z, position grids
    #xgrid = np.arange(dose.ImagePositionPatient[0], dose.Rows, dose.PixelSpacing[0])
    #ygrid = np.arange(dose.ImagePositionPatient[1], dose.Columns, dose.PixelSpacing[1])
    #zgrid = np.arange(dose.ImagePositionPatient[2], dose.NumberOfFrames, int(dose.GridFrameOffsetVector[1-0]))

    # How to build grid? Linearly spaced?
    xgrid = np.linspace(-200, 200, 400)
    ygrid = np.linspace(-200, 200, 400)
    zgrid = np.linspace(-200, 200, 400)

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

    '''
    def printDoseGradient(level):
        gradlevel = gradnorm[level]
        doselevel = dose.pixel_array[level]
    
        plt.imshow(doselevel)
        plt.quiver(grad[0][100], grad[1][100], grad[2][100])
    '''

    # minimum dose in Gy
    dosethreshold = threshold / 100.
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
    return sortedpoints

'''
def printpoints(numOfPoints):
    

    for i in range(numOfPoints):
        print("({:.2f}, {:.2f}, {:.2f}) : {:.1f} cGy Gradient = {}".format(
            sortedpoints[i][0] / 10,
            (sortedpoints[i][1] + np.max(ygrid)) / 10,
            sortedpoints[i][2] / 10,
            sortedpoints[i][3],
            sortedpoints[i][4]
        ))
'''

def sortByDepth():
    sortedpoints = sorted(points, key=lambda x: x[1])
    return sortedpoints

def sortByGradient():
    sortedpoints = sorted(points, key=lambda x: x[4])
    return sortedpoints

def sortByDose():
    sortedpoints = sorted(points, key=lambda x: x[3], reverse=True)
    return sortedpoints

def load_file():

    filename = filedialog.askopenfilename(initialdir="/",
                                          title="Select file",
                                          filetypes=(("DICOM files", "*.dcm"), ("All files", "*.*")))
    path.set(filename)

    return filename

def run():

    fname = path.get()
    points = int(numOfPoints.get())
    threshold = int(doseThreshold.get())

    dosegradient(fname, points, threshold)


    print(fname)
    print("Completed using {} points and {}% dose threshold".format(points, threshold))

root = Tk()

#root.geometry('{}x{}'.format(300, 300))
root.resizable(False, False)
root.title("Point Dose Selector")

loadDICOM = Button(root, text="Browse for DICOM", command=load_file)
loadDICOM.grid(row=1, column=1, padx=5, pady=5)

path = StringVar()
dcmLbl = Label(root, text=path, textvariable=path)
dcmLbl.grid(row=1, padx=5, pady=5)

numOfPoints = Entry(root)
numOfPoints.grid(row=2, padx=5, pady=5, sticky=E)

pointsLbl = Label(root, text="Enter desired number of points")
pointsLbl.grid(row=2, column=1, padx=5, pady=5, sticky=W)

doseThreshold = Entry(root)
doseThreshold.grid(row=3, padx=5, pady=5, sticky=E)

thresholdLbl = Label(root, text="Enter % of Dose Max")
thresholdLbl.grid(row=3, column=1, padx=5, pady=5, sticky=W)

runBtn = Button(root, text="Run", command=run)
runBtn.grid(row=4, column=1, padx=5, pady=5)

# Build data table
table = ttk.Treeview(root)
table.grid(row=5, column=1, padx=5, pady=5, sticky=E)
table["columns"] = ("x", "y", "z", "Dose", "Gradient")
table.column("x", width=100)
table.column("y", width=100)
table.column("z", width=100)
table.column("Dose", width=100)
table.column("Gradient", width=100)

table.heading("x", text="x(cm)")
table.heading("y", text="y(cm)")
table.heading("z", text="z(cm)")
table.heading("Dose", text="Dose(cGy)")
table.heading("Gradient", text="Gradient")





mainloop()