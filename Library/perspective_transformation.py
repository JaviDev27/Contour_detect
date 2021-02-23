import cv2 as cv
import numpy as np


class Perspective:

    def __init__(self, image, width, height):
        self.image = image
        self.width = width
        self.height = height
        self.firstPoints = None

    def perspectiveShow(self):

        # Se coloca primero los puntos de la imagen a mover
        """ Considera el orden de los puntos
        punto1   punto2
            -------
            |       |
            |       |
            -------
        punto3   punto4
        """

        secondsPoint = np.float32(
            [[0, 0],
             [self.width, 0],
             [0, self.height],
             [self.width, self.height]])

        matrixM = cv.getPerspectiveTransform(self.firstPoints, secondsPoint)

        dts = cv.warpPerspective(self.image, matrixM,
                                 (self.width, self.height))
        return dts

    def __order_points(self, points):
        n_points = np.concatenate(
            [points[0], points[1], points[2], points[3]]).tolist()

        y_order = sorted(n_points, key=lambda n_points: n_points[1])

        x1_order = y_order[:2]
        x1_order = sorted(x1_order, key=lambda x1_order: x1_order[0])

        x2_order = y_order[2:4]
        x2_order = sorted(x2_order, key=lambda x2_order: x2_order[0])

        return [x1_order[0], x1_order[1], x2_order[0], x2_order[1]]

    def roi_imagen(self):

        perspectiva = None

        image_copy = self.image.copy()

        gray = cv.cvtColor(image_copy, cv.COLOR_BGR2GRAY)
        _, th = cv.threshold(gray, 80, 255, 0)

        contours = cv.findContours(
            th, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)[0]
        contours = sorted(contours, key=cv.contourArea, reverse=True)[:1]

        for c in contours:
            epsilon = 0.01*cv.arcLength(c, True)
            approx = cv.approxPolyDP(c, epsilon, True)
            if len(approx) == 4:
                points = self.__order_points(approx)
                self.firstPoints = np.float32(points)
                perspectiva = self.perspectiveShow()

        return perspectiva
