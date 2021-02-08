import cv2 as cv
import numpy as np

path_image = '../imagen_examples/corazon.jpg'
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
    cv.imshow(origin_name, imagen)


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
    imagen = cv.imread(path_image, cv.IMREAD_COLOR)


if __name__ == '__main__':
    imagen = cv.imread(path_image, cv.IMREAD_COLOR)

    update_screen()
    cv.setMouseCallback(origin_name, select_points)

    while True:

        if len(points) == 4:
            pass

        key = cv.waitKey(1)
        if key == 27:  # Press ESC to finish
            break
        elif key == 114:  # Press r to reset
            reset_points()

    cv.destroyAllWindows()
