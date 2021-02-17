import cv2 as cv
import numpy as np


class Perspective:

    def __init__(self, imagen, points):
        self.imagen = imagen
        self.points = points

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
        # Se toma el tamaño de la imagen original
        height, width, channel = self.imagen.shape

        # Aqui se hace un acorrección de la logica debido a que cambia la ubicación de los puntos
        firstPoints = np.float32(
            [self.points[0], self.points[1], self.points[3], self.points[2]])

        secondsPoint = np.float32(
            [[0, 0],
             [width, 0],
             [0, height],
             [width, height]])

        matrixM = cv.getPerspectiveTransform(firstPoints, secondsPoint)

        dts = cv.warpPerspective(self.imagen, matrixM, (width, height))

        cv.imshow('Perspectiva', dts)

        return dts
