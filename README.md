# Contour Detect

---

_Project to detect the contour of objects in 2d made in python with OpenCv_

### Pre-requisites 📋

_You need install_

```shell
pip install opencv-python-headless
pip install matplotlib
pip install ezdxf
pip install imutils
pip install ipython
```

if you work in windows install GTK+ 2.x or Cocoa support. Or you are on Ubuntu or Debian, install libgtk2.0-dev and pkg-config, then re-run cmake or configure script in function 'cvShowImage'

## Calibrate CAM ⚙️

_You need run main.py to generate the date calibrations. The project have examples of picture in the **imagen_calibration folder**_

```shell
python main.py
```

_The script detect the points in the chessboard_
![Imgur](https://i.imgur.com/TwHpRa1.png)

Finally the data is save in _file_calibration folder_

Run the _perpective_main.py_ to change de perspective and have the contour.
![Imgur](https://i.imgur.com/44pPBu4.png)

The script generated a file .dxf with the different points of the contour.

## Autors ✒️

- **Javier Manobanda** - _Initial Work_ - [Github](https://github.com/JaviManobanda)

## License 📄

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

⌨️ with ❤️ by [Javier Manobanda](https://github.com/JaviManobanda) 😊
