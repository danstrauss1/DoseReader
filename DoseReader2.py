import numpy as np
import pydicom

class DoseCube:

    def __init__(self, dicom):
        self.dicom = dicom


    def dosegradient(self):
        dicom = pydicom.dcmread(self.dicom)

        dosematrix = dicom.pixel_array
        gradmatrix = np.gradient(dicom.pixel_array)
        dosethreshold = 0.5 * np.max(dicom.pixel_array)
        index = np.where(dicom.pixel_array >= dosethreshold)

        points = dicom.pixel_array[index]


        return dosematrix, gradmatrix, points

    def dosethreshold(self):
        dicom = pydicom.dcmread(self.dicom)
        dosethreshold = 0.5 * np.max(dicom.pixel_array)

        index = np.where(dicom.pixel_array >= dosethreshold)

        return index
        #Find indicies which satisfy dose >= dosetheshold

file = r"C:\Users\User\Documents\DoseVolumeTest\DoseVolumeTest.dcm"

def main():
    #gradmatix = DoseCube(file).dosegradient()
    #dosethreshold = DoseCube(file).dosethreshold()
    #print(gradmatix)
    #print("Maximum Gradient is: {}.".format(np.max(gradmatix)))
    #print("Viable indicies are {}.".format(dosethreshold))

    dosematrix, gradmatix, points = DoseCube(file).dosegradient()
    print("Viable points are {}".format(points))
main()