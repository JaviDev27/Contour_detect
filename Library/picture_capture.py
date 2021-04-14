import cv2 as cv
import numpy as np


if __name__ == '__main__':
    image = cv.VideoCapture(0)
    count = 0
    header_imagen = 'chess_'

    if not image.isOpened():
        print('Dont open camera')

    while True:

        ret, frame = image.read()

        if ret:
            cv.imshow('Image_Capture', frame)
            key = cv.waitKey(1)
            if key == 112:
                cv.imwrite(
                    '../imagen_examples/chess_v2/{0}{1}.jpg'.format(header_imagen, count), frame)
                print('Se almacena la imagen: {0}{1}'.format(
                    header_imagen, count))
                count += 1
            elif key == 27:
                break
            elif count > 14:
                break

    print('Se termina el proceso de captura')
