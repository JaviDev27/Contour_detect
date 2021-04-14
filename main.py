from Library.bed_calibration import *
from Library.read_image import *
import cv2 as cv

if __name__ == '__main__':
    cali = Calibrate(1, 30)

    cali.init_calibration_bed('./images_calibration', 'jpg', 18)
    cali.save_coefficientes('./file_calibration', 'calibration')

    print('valor ret ', cali.data_calibrate.ret)
    print('valor mtx ', cali.data_calibrate.mtx)
    print('valor dist ', cali.data_calibrate.dist)
    print('valor rvecs ', cali.data_calibrate.rvecs)
    print('valor tvecs ', cali.data_calibrate.tvecs)
