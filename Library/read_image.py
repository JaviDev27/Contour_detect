import cv2 as cv
import numpy as np
from .perspective_transformation import Perspective
from .bed_calibration import *

path_image = '../imagen_examples/cat.jpg'
origin_name = 'Origin'
color_point = (0, 255, 0)
color_line = (0, 0, 255)
points = []


def select_points(event, x, y, flags, param):
    """Function to draw points to cut the imagen

    Args:
        event (event): event OpenCv
        x (int): x axis
        y (int): y axis
        flags ([type]): [description]
        param ([type]): [description]
    """
    radius = 5
    thickness = 2
    global points

    if event == cv.EVENT_LBUTTONDOWN:
        cv.circle(imagen, (x, y), radius, color_point, thickness)
        points.append((x, y))
        print(x, "--", y, "__", len(points))

        if len(points) > 1:
            join_points(points[len(points)-2], points[len(points)-1])
            print(points[len(points)-2], "_____", points[len(points)-1])

        if len(points) == 4:
            join_points(points[0], points[3])

        update_screen()


def update_screen():
    cv.imshow(origin_name, dst)


def join_points(point_1, point_2):
    """ Joint 2 points

    Args:
        point_1 (tuple (x,y)): first point
        point_2 (tuple (x,y)): second point
    """
    thickness = 1
    cv.line(imagen, point_1, point_2, color_line, thickness)


def reset_points():
    points.clear()
    update_screen()


if __name__ == '__main__':

    cali = Calibrate()
    # cargo los coeficientes para esta camara
    cali.load_coefficientes('../file_calibration/calibration_v2.pckl')

    imagen = cv.imread(path_image, cv.IMREAD_COLOR)  # leo imagen original

    new_camera_mtx, roi = cv.getOptimalNewCameraMatrix(
        cali.data_calibrate.mtx, cali.data_calibrate.dist, imagen.shape[1::-1], 1, None, None)

    dst = cv.undistort(imagen, cali.data_calibrate.mtx,
                       cali.data_calibrate.dist, None, new_camera_mtx)

    """scalePercent = 0
    width = int(imagen.shape[1]*scalePercent/100)
    height = int(imagen.shape[0]*scalePercent/100)
    resized = cv.resize(imagen, (width, height), interpolation=cv.INTER_AREA)
    imagen = resized"""

    copyImagen = dst.copy()  # have a copy of te imagen

    update_screen()
    cv.setMouseCallback(origin_name, select_points)

    while True:

        if len(points) == 4:

            key = cv.waitKey(1)
            if key == 27:  # Press ESC to finish
                break
            elif key == 114:  # Press r to reset
                dst = copyImagen.copy()
                reset_points()
            elif key == 112:  # Press p to change perspective
                changePerspective = Perspective(copyImagen, points)
                changePerspective.perspectiveShow()

    cv.destroyAllWindows()
