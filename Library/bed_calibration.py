from IPython.display import display
import cv2 as cv
import numpy as np
import glob
import pickle


class Data_Calibrate:
    """Clase de los datos para la calibración de la cama
    """

    def __init__(self):
        self.ret = None
        self.mtx = None
        self.dist = None
        self.rvecs = None
        self.tvecs = None


class Calibrate:
    """Clase que sirve para calibrar la cama
    """

    def __init__(self, wait=1, scalePercent=100):
        self.wait = wait
        self.scalePercent = scalePercent
        # Variables of the class
        self.data_calibrate = Data_Calibrate()

    def init_calibration_bed(self, dir_path_images, imagen_format, square_size, width=9, heigth=6):
        """Método para iniciar la calibración de la cama

        Args:\n
            - dir_path_images (string): dirección de las imágenes solo el path de la carpeta
            - imagen_format (string): tipo de formato de las imágenes ejm. jpg, png
            - square_size (int): tamaño en mm de los cuadrados del tablero
            - width (int, optional): numero de columnas del tablero. Defaults to 9.
            - heigth (int, optional): número de filas del tablero. Defaults to 6.
        """

        # Se toma todas las imagenes de un mismo directorio que terminen
        images = glob.glob(dir_path_images + '/*.'+imagen_format)
        # con una extención específica.
        # Termino criterio esto es recomendado por openCv
        criteria = (cv.TERM_CRITERIA_EPS +
                    cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

        # preparar puntos de objeto, como (0,0,0,0), (1,0,0,0), (2,0,0,0)...., (6,5,0)
        # Genera una matriz de (mxn) de valores float32
        objp = np.zeros((width*heigth, 3), np.float32)
        objp[:, :2] = np.mgrid[0:width, 0:heigth].T.reshape(-1, 2)

        objp = objp*square_size  # Multiplica por el tamaño del cuadro.

        # Se crea array de los puntos del objeto a encontrar y de la imagen.
        objpoints = []  # puntos de objeto en 3d
        imgpoints = []  # puntos 2d en la imagen

        print('Calibration Beb Start ____')
        print('Files numbers:', len(images))

        count_images = 0  # count the files

        # Se recorre cada imagen del directorio
        for fname in images:
            img = cv.imread(fname)
            # hago un resize de la imagen

            width_img = int(img.shape[1]*self.scalePercent/100)
            height_img = int(img.shape[0]*self.scalePercent/100)
            resized = cv.resize(img, (width_img, height_img),
                                interpolation=cv.INTER_AREA)
            print(width_img, height_img)
            img = resized

            # transforma a escala de grises
            img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

            # Encuentra las esquinas del tablero de ajedrez
            ret, corners = cv.findChessboardCorners(
                img_gray, (width, heigth), None)
            count_images += 1
            # display status calibration
            print('Find Countors : {0} of {1} is {2} __ File name: {3}'.format(
                count_images, len(images), ret, fname))

            # Si se encuentran, añada puntos de objeto, puntos de imagen (después de refinarlos)
            if ret == True:
                objpoints.append(objp)  # Se agrega puntos de objeto ala array

                corners2 = cv.cornerSubPix(
                    img_gray, corners, (11, 11), (-1, -1), criteria)  # Aumenta la precisión

                imgpoints.append(corners2)

                # Dibuja y muestra las esquinas
                # dibuja el patron encontrado
                img = cv.drawChessboardCorners(
                    img, (width, heigth), corners2, ret)

                cv.imshow('img', img)
                cv.waitKey(self.wait)

        self.data_calibrate.ret, self.data_calibrate.mtx, self.data_calibrate.dist, self.data_calibrate.rvecs, self.data_calibrate.tvecs = cv.calibrateCamera(
            objpoints, imgpoints, img_gray.shape[::-1], None, None)

    def save_coefficientes(self, path_coefficientes, name_file):
        """Método para guardar los coeficientes de calibración

        Args:
            path_coefficientes (string): dirección de la carpeta
            name_file (string): nombre del archivo
        """
        path = '{0}/{1}.pckl'.format(path_coefficientes, name_file)
        print(path)
        file = open(path, 'wb')
        pickle.dump(self.data_calibrate, file)
        file.close()

    def load_coefficientes(self, path_coefficientes):
        """Carga los coeficientes de calibración de la cama

        Args:
            path_coefficientes (string): dirección del archivo
        """
        file = open(path_coefficientes, 'rb')
        self.data_calibrate = pickle.load(file)
        file.close()


if __name__ == '__main__':
    cali = Calibrate()
    cali.init_calibration_bed('../imagen_examples/camera_francisco', 'jpg', 18)
    cali.save_coefficientes('../file_calibration', 'calibration_francisco')
    # cali.load_coefficientes('../file_calibration/calibration.pckl')

    print(cali.data_calibrate.mtx)
