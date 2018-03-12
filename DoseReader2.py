import numpy as np
import pydicom

class DoseCube:


    def __init__(self, dicom):
        self.dicom = dicom

    '''
    def dosegradient(self):

        ds = pydicom.dcmread(self.dicom)


        gradmatrix = np.gradient(ds.pixel_array)
        dosethreshold = 0.5 * np.max(ds.pixel_array)
        index = np.where(ds.pixel_array >= dosethreshold)

        points = ds.pixel_array[index]


        return gradmatrix

    def dosethreshold(self, mindose):
        ds = pydicom.dcmread(self.dicom)
        dosethreshold = mindose * np.max(ds.pixel_array)

        index = np.where(ds.pixel_array >= dosethreshold)

        return index
    '''

    def dosegradient(self, threshold, num_of_points):

        dose = pydicom.dcmread(self.dicom)

        maxdose = np.max(dose.pixel_array)

        Position = dose.data_element("Image Position (Patient)")
        PixelSpacing = dose.data_element("Pixel Spacing")
file = r"C:\Users\User\Documents\DoseVolumeTest\DoseVolumeTest.dcm"

def main():


    gradmatrix = DoseCube(file).dosegradient(0.5, 100)
    print("Viable points are {}".format(points))
    #for point in points:
        #print("Point : {}".format(point))
main()