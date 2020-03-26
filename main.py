from PyQt5 import QtWidgets
from <...> import Ui_MainWindow 
# replace <...> with your py file generate from pyuic5 command - without .py-

# It's preferaple to work on MainWindow in qt designer to support layouts
# use Dialog for relatively small windows or windows that don't have too much elements  

import sys

from imageModel import ImageModel

class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ApplicationWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


def main():
    app = QtWidgets.QApplication(sys.argv)
    application = ApplicationWindow()
    application.show()
    app.exec_()


if __name__ == "__main__":
    main()