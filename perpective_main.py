import cv2 as cv
import numpy as np
from Library.perspective_transformation import Perspective
from Library.bed_calibration import *
import matplotlib.pyplot as plt
import ezdxf as dxf
import imutils

#path_image = './imagen_examples/camera_francisco/examples/IMG_4675.JPG'
#path_image = './imagen_examples/piezapuerta.jpg'
path_image = './imagen_examples/figures_geome2.jpg'
#path_calibration = './file_calibration/calibration_franciscov3.pckl'
path_calibration = './file_calibration/calibration_v3.pckl'
origin_name = 'Origin'


if __name__ == '__main__':
    # Size of the sheet
    heigh_sheet = 210
    width_sheet = 297

    cali = Calibrate()
    # cargo los coeficientes para esta camara
    cali.load_coefficientes(path_calibration)

    imagen = cv.imread(path_image)  # leo imagen original

    # hago un resize de la imagen
    imagen = imutils.resize(imagen, width=1080)
    width_img = imagen.shape[1]
    height_img = imagen.shape[0]

    # Use te matrix camera first use a optimization
    new_camera_mtx, roi = cv.getOptimalNewCameraMatrix(
        cali.data_calibrate.mtx, cali.data_calibrate.dist, imagen.shape[1::-1], 1, None, None)

    dst = cv.undistort(imagen, cali.data_calibrate.mtx,
                       cali.data_calibrate.dist, None, new_camera_mtx)

    copyImagen = dst.copy()  # have a copy of te imagen

    # Detect contour of sheet
    chang_persp = Perspective(copyImagen, 720, 509)
    image_perspectiva = chang_persp.roi_imagen()

    cv.imshow('Change Perspective', image_perspectiva)

    # Desde aqui empieza a buscar el contorno

    # change to BGR scale IN hsv cv.COLOR_BGR2HSV
    img_perpec_HSV = cv.cvtColor(image_perspectiva, cv.COLOR_BGR2HSV)
    img_gauss = cv.GaussianBlur(img_perpec_HSV, (3, 3), 0)
    print(img_gauss.shape)

    # hsv

    # here change the contrast an saturation to find the object contour
    lower = np.array([8, 30, 30])
    higher = np.array([50, 250, 250])
    ''' PANCHO '''
    ''' lower = np.array([120, 60, 30])
    higher = np.array([250, 150, 100]) '''
    ''' PANCHO '''
    #lower = np.array(90)
    #higher = np.array(250)
    mask = cv.inRange(img_gauss, lower, higher)

    ret, thresh = cv.threshold(mask, 127, 255, 0)

    contour, _ = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    # white image to draw the contour find use the size of the image with the perspective change
    width_persp = img_gauss.shape[1]
    heigh_persp = img_gauss.shape[0]
    contor_conten = np.ones(
        (heigh_persp, width_persp), np.float32)

    img_contour = cv.drawContours(
        contor_conten, contour, -1, (0, 0, 255), 2)

    cv.imshow('con', img_contour)

    plt.figure(figsize=(9, 9))

    plt.subplot(2, 2, 1), plt.imshow(imagen, 'gray'), plt.title('Origin')
    plt.subplot(2, 2, 2), plt.imshow(img_perpec_HSV), plt.title('Perspective')
    plt.subplot(2, 2, 3), plt.imshow(mask), plt.title('Mask')
    plt.subplot(2, 2, 4), plt.imshow(img_contour), plt.title('Contour')
    plt.show()

    # created a new document
    doc = dxf.new(dxfversion='R2010')
    model = doc.modelspace()
    doc.layers.new(name='Countour', dxfattribs={'color': 2})

    for line in contour:

        count = 0
        first_point = [abs((line[0][0][0]*heigh_sheet) / heigh_persp),
                       abs((line[0][0][1]*width_sheet)/width_persp)]

        while True:

            point_1 = [abs((line[count][0][0]*heigh_sheet) / heigh_persp),
                       abs((line[count][0][1]*width_sheet)/width_persp)]

            point_2 = [abs((line[count + 1][0][0]*heigh_sheet) / heigh_persp),
                       abs((line[count + 1][0][1]*width_sheet)/width_persp)]

            model.add_line(point_1, point_2, dxfattribs={'layer': 'MyLines'})

            if count == len(line) - 2:
                model.add_line(point_2, first_point,
                               dxfattribs={'layer': 'MyLines'})
                break
            else:
                count += 1

    doc.saveas('./countor.dxf')

    cv.waitKey(0)

    cv.destroyAllWindows()
