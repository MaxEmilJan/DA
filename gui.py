from PyQt5 import QtWidgets, QtGui, QtCore
import sys
import cv2 as cv
import numpy as np

class rent_a_cam(QtWidgets.QMainWindow):
    def __init__(self):
        super(rent_a_cam, self).__init__()
        self.resize(1200,800)
        self.setGeometry(0, 0, 1200, 800)
        self.setWindowTitle('rent a cam')
        self.initUI()
        
    def initUI(self):
        # labels
        self.label_titel = QtWidgets.QLabel(self)
        self.label_titel.setGeometry(QtCore.QRect(30, 10, 171, 51))
        self.label_titel.setFont(QtGui.QFont("Arial", 24, QtGui.QFont.Bold))
        self.label_titel.setObjectName("label_titel")
        self.label_titel.setText("rent a cam")
        self.label_cam = QtWidgets.QLabel(self)
        self.label_cam.setGeometry(QtCore.QRect(50, 550, 171, 51))
        self.label_cam.setFont(QtGui.QFont("Arial", 24, QtGui.QFont.Bold))
        self.label_cam.setObjectName("label_cam")
        self.label_cam.setText("Kamera:")
        self.label_camnumber = QtWidgets.QLabel(self)
        self.label_camnumber.setGeometry(QtCore.QRect(250, 550, 91, 51))
        self.label_camnumber.setFont(QtGui.QFont("Arial", 24, QtGui.QFont.Bold))
        self.label_camnumber.setObjectName("label_camnumber")
        self.label_camnumber.setText("####")
        self.label_list = QtWidgets.QLabel(self)
        self.label_list.setGeometry(QtCore.QRect(930, 10, 191, 51))
        self.label_list.setFont(QtGui.QFont("Arial", 24, QtGui.QFont.Bold))
        self.label_list.setObjectName("label_list")
        self.label_list.setText("Kürzel User:")
        self.label_status = QtWidgets.QLabel(self)
        self.label_status.setGeometry(QtCore.QRect(960, 750, 200, 20))
        self.label_status.setAlignment(QtCore.Qt.AlignRight)
        self.label_status.setFont(QtGui.QFont("Arial", 15, QtGui.QFont.Bold))
        self.label_status.setObjectName("label_status")
        self.label_status.setText("------")
        # buttons to rent, return, repeat or cancel
        self.button_rent = QtWidgets.QPushButton(self)
        self.button_rent.setGeometry(QtCore.QRect(50, 650, 191, 121))
        self.button_rent.setStyleSheet("background-color: rgb(30, 100, 30); font: 20pt \"Noto Sans\";")
        self.button_rent.setObjectName("button_rent")
        self.button_rent.setText("Kamera\nausleihen")
        self.button_rent.clicked.connect(self.rentclicked_event)
        self.button_return = QtWidgets.QPushButton(self)
        self.button_return.setGeometry(QtCore.QRect(260, 650, 191, 121))
        self.button_return.setStyleSheet("background-color: rgb(100, 30, 30); font: 20pt \"Noto Sans\";")
        self.button_return.setObjectName("button_return")
        self.button_return.setText("Kamera\nzurückgeben")
        self.button_return.clicked.connect(self.returnclicked_event)
        self.button_repeat = QtWidgets.QPushButton(self)
        self.button_repeat.setGeometry(QtCore.QRect(470, 650, 191, 121))
        self.button_repeat.setStyleSheet("background-color: rgb(150, 85, 0); font: 20pt \"Noto Sans\";")
        self.button_repeat.setObjectName("button_repeat")
        self.button_repeat.setText("erneut\nscannen")
        self.button_repeat.clicked.connect(self.repeatclicked_event)
        self.button_cancel = QtWidgets.QPushButton(self)
        self.button_cancel.setGeometry(QtCore.QRect(680, 650, 191, 121))
        self.button_cancel.setStyleSheet("background-color: rgb(30, 30, 30); font: 20pt \"Noto Sans\";")
        self.button_cancel.setObjectName("button_cancel")
        self.button_cancel.setText("abbrechen")
        self.button_cancel.clicked.connect(self.cancelclicked_event)
        # screen to display the output image of main.py
        self.screen = QtWidgets.QGraphicsView(self)
        self.screen.setGeometry(QtCore.QRect(30, 70, 871, 441))
        self.screen.setObjectName("screen")
        # list to choose user
        self.list = QtWidgets.QListWidget(self)
        self.list.setGeometry(QtCore.QRect(930, 70, 235, 650))
        self.list.setSortingEnabled(True)
        self.list.setDragEnabled(False)
        self.list.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.list.setObjectName("list")
        item = QtWidgets.QListWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(20)
        item.setFont(font)
        item.setText("asb")
        self.list.addItem(item)
        item = QtWidgets.QListWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(20)
        item.setFont(font)
        item.setText("mbec")
        self.list.addItem(item)
        item = QtWidgets.QListWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(20)
        item.setFont(font)
        item.setText("trc")
        self.list.addItem(item)
        item = QtWidgets.QListWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(20)
        item.setFont(font)
        item.setText("srec")
        self.list.addItem(item)
        self.list.itemClicked.connect(self.listClicked_event)
    
    def listClicked_event(self):
        item = self.list.selectedItems()[0]
        self.label_status.setText(str(item.text()))
        self.label_status.adjustSize()
        
    def rentclicked_event(self):
        self.label_status.setText("Kamera ausgeliehen")
        self.label_status.setAlignment(QtCore.Qt.AlignRight)
        self.label_status.adjustSize()
        
    def returnclicked_event(self):
        self.label_status.setText("Kamera zurückgegeben")
        self.label_status.setAlignment(QtCore.Qt.AlignRight)
        self.label_status.adjustSize()
        
    def repeatclicked_event(self):
        self.label_status.setText("scannen...")
        self.label_status.setAlignment(QtCore.Qt.AlignRight)
        self.label_status.adjustSize()
        
    def cancelclicked_event(self):
        self.label_status.setAlignment(QtCore.Qt.AlignRight)
        self.label_status.setText("Vorgang abgebrochen")
        self.label_status.adjustSize()
        
        
        
def window():
    app = QtWidgets.QApplication(sys.argv)
    win = rent_a_cam()
    win.show()
    sys.exit(app.exec_())

# load vignetting_correction_mask.npy to work with this array
vignett_mask = np.load("vignetting_correction/vignetting_correction_mask.npy")
# create the necessary filters for morphologic operations
filter_close = cv.getStructuringElement(cv.MORPH_RECT, (3,3))
filter_dil = cv.getStructuringElement(cv.MORPH_RECT, (51,51))

window()
