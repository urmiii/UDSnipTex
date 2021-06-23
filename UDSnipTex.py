from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import QApplication, QMainWindow, QComboBox, QLabel, QPushButton, QGroupBox
from PyQt5.QtGui import QIcon
import tkinter as tk
from PIL import ImageGrab
import cv2
import numpy as np
import pytesseract
import pyperclip


    
class Communicate(QObject):
    
    snip_saved = pyqtSignal()
    
class Ui_MainWindow(object):
    
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("UDSnipTex")
        MainWindow.resize(800, 600)
     
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(560, 0, 91, 31))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(130, 0, 91, 31))
        self.pushButton_2.setObjectName("pushButton_2")
        self.columnView = QtWidgets.QColumnView(self.centralwidget)
        self.columnView.setGeometry(QtCore.QRect(10, 30, 391, 521))
        self.columnView.setObjectName("columnView")
        self.columnView_2 = QtWidgets.QColumnView(self.centralwidget)
        self.columnView_2.setGeometry(QtCore.QRect(390, 30, 401, 521))
        self.columnView_2.setObjectName("columnView_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(400, 30, 231, 160))
        self.label.setObjectName("label")
        
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 30, 231, 160))
        self.label_2.setObjectName("label_2")
        Ui_MainWindow.label_2 = self.label_2
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(340, 0, 91, 31))
        self.pushButton_3.setObjectName("pushButton_3")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        self.menuUDSnipTex = QtWidgets.QMenu(self.menubar)
        self.menuUDSnipTex.setObjectName("menuUDSnipTex")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menuUDSnipTex.addSeparator()
        self.menuUDSnipTex.addSeparator()
        self.menubar.addAction(self.menuUDSnipTex.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.pushButton_2.clicked.connect(self.snip_copy_clicked) 
        self.pushButton.clicked.connect(SnipWidget.copyNew)
        self.pushButton_3.clicked.connect(lambda:MainWindow.close())

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "UDSnipTex"))
        MainWindow.setWindowIcon(QIcon("logo.png")) 
        self.pushButton.setText(_translate("MainWindow", "Copy"))
        self.pushButton_2.setText(_translate("MainWindow", "New"))
        self.label.setText(_translate("MainWindow", "Image"))
        self.label_2.setText(_translate("MainWindow", "Image Text"))
        self.pushButton_3.setText(_translate("MainWindow", "Exit"))
        
    def snip_copy_clicked(self):
        self.snipWin = SnipWidget( True,  self)
        self.snipWin.notification_signal.connect(self.reset_notif_text)
        self.snipWin.show()
        self.label_2.setText("Snipping... Press ESC to quit snipping")
        self.update_notif()
    
    def reset_notif_text(self):
        self.label.setText("")
        self.update_notif()
        
    def update_notif(self):
        self.label.move(400, 155)
        self.label.adjustSize()
        
class SnipWidget(QMainWindow,Ui_MainWindow):
    
    notification_signal = pyqtSignal()
    
    def __init__(self,  copy_str , parent):
        super(SnipWidget, self).__init__()
        
        self.copy_str = copy_str
        root = tk.Tk()# instantiates window
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        self.setGeometry(0, 0, screen_width, screen_height)
        self.setWindowTitle(' ')
        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()
        self.setWindowOpacity(0.3)
        self.is_snipping = False
        QtWidgets.QApplication.setOverrideCursor(
            QtGui.QCursor(QtCore.Qt.CrossCursor)
        )
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.c = Communicate()
        
        
        self.show()
        
       
        if self.copy_str == True:
            self.c.snip_saved.connect(self.IdAndCopy)

    

            
    def paintEvent(self, event):
        if self.is_snipping:
            brush_color = (0, 0, 0, 0)
            lw = 0
            opacity = 0
        else:
            brush_color = (128, 128, 255, 128)
            lw = 3
            opacity = 0.3

        self.setWindowOpacity(opacity)
        qp = QtGui.QPainter(self)
        
        qp.setPen(QtGui.QPen(QtGui.QColor('black'), lw))
        qp.setBrush(QtGui.QColor(*brush_color))
        qp.drawRect(QtCore.QRect(self.begin, self.end))
        
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            print('Quit')
            QtWidgets.QApplication.restoreOverrideCursor();
            self.notification_signal.emit()
            self.close()
        event.accept()

    def mousePressEvent(self, event):
        self.begin = event.pos()
        self.end = self.begin
        self.update()

    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.update()

    def mouseReleaseEvent(self, event):
        x1 = min(self.begin.x(), self.end.x())
        y1 = min(self.begin.y(), self.end.y())
        x2 = max(self.begin.x(), self.end.x())
        y2 = max(self.begin.y(), self.end.y())
        self.is_snipping = True        
        self.repaint()
       
        QtWidgets.QApplication.processEvents()
        img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        
        self.is_snipping = False
        self.repaint()
        QtWidgets.QApplication.processEvents()
        img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2GRAY)
       
        self.snipped_image = img
        QtWidgets.QApplication.restoreOverrideCursor();
        self.c.snip_saved.emit()
        self.close()
        self.msg = 'snip complete'
        self.notification_signal.emit()
        
        
  
        
    def IdAndCopy(self):
        
        img_str = self.imgToStr(self.snipped_image)
        
        
        
    pytesseract.pytesseract.tesseract_cmd='C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'
    def find_str(self, image_data):
       
        
        img = image_data
        
        h,w = np.shape(img)
        asp_ratio = float(w/h)
        img_width = 500
        img_height = int(round(img_width/asp_ratio))
        desired_image_size = (img_width,img_height)
        img_resized = cv2.resize(img, desired_image_size)
        
        
        imgstr = str(pytesseract.image_to_string(img_resized))
        
        Ui_MainWindow.label_2.setText(imgstr)
        global text
        text= imgstr
        
        
        return imgstr
        
    def copyNew():
        global text
       
        pyperclip.copy(text)
        
        
    def imgToStr(self, image):
        # img_str = imageToString.main(image)
        img_str = self.find_str(image)
        return img_str
    
        
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
   
    MainWindow.show()
    sys.exit(app.exec_())
