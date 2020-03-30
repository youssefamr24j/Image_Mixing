# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Mixerupdate.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!
import logging
import cv2
from PyQt5 import QtCore, QtGui, QtWidgets
from pyqtgraph import PlotWidget
import numpy as np
import pyqtgraph as pg
from scipy.fftpack import fft,fft2,fftn,fftshift,ifft2
from numpy.fft import fft,fftfreq,ifft,fft2,fftn,fftshift,ifft2
from operator import add

logging.basicConfig(filename='AppSimulation.log',level=logging.INFO ,format='%(message)s where levelname is%(levelname)s ')

class Image:
    def __init__(self):
        self.ImageObject=[]
        self.Magnitude=[]
        self.Phase=[]
        self.Real=[]
        self.Imaginary=[]
        

    def SetImage(self,directory):
        self.ImageObject= cv2.imread(directory,cv2.IMREAD_GRAYSCALE)
        self.ImageObject=np.rot90(self.ImageObject,3)

    def CheckEqual(self,Image):
        if(((len(self.ImageObject[:,0])) == (len(Image.getImage()[:,0])) and ((len(self.ImageObject[0,:])) == (len(Image.getImage()[0,:])) ))):
            return True
        return False

    def CheckEmpty(self):
        if( self.ImageObject == [] ):
            return True
        return False    

    def EmptyImage(self):
        self.ImageObject =[]


    def DisplayImage(self):
        View = pg.ImageItem(self.ImageObject)
        return View

    def DisplayImageMag(self):
        self.setMagnitude()
        View = pg.ImageItem(self.getMagnitude())
        return View
    
    def DisplayImagePhase(self):
        self.setPhase()
        View = pg.ImageItem(self.getPhase())
        return View
        

    def DisplayImageReal(self):
        self.setReal()
        View = pg.ImageItem(self.getReal())
        return View
       

    def DisplayImageImag(self):
        self.setImaginary()
        View = pg.ImageItem(self.getImaginary())
        return View

    def MixingMagPhase(self,Image,W1,W2):
        self.setMagnitude()
        self.setPhase()
        Image.setMagnitude()
        Image.setPhase()
        TempMagnitude=list(map(add, ((W1)*(np.array(self.getMagnitude()))),((1-W1)*(np.array(Image.getMagnitude())))))
        TempPhase=np.exp(list(map(add, ((W2)*(np.array(Image.getPhase()))), ((1-W2)*(np.array(self.getPhase())))) ))
        Mix=[a*b for a,b in zip(TempMagnitude,TempPhase)]
        View = ifft2(Mix)
        View =np.real(View)
        View = pg.ImageItem(View)
        return View

    def MixingMagUniPhase(self,Image,W1,W2):
        self.setMagnitude()
        self.setPhase()
        Image.setMagnitude()
        Image.setPhase()
        TempMagnitude=list(map(add, ((W1)*(np.array(self.getMagnitude()))),((1-W1)*(np.array(Image.getMagnitude())))) )
        TempPhase=np.exp(list(map(add, ((0)*(np.array(Image.getPhase()))), ((1-W2)*(np.array(self.getPhase())))) ))
        Mix=[a*b for a,b in zip(TempMagnitude,TempPhase)]   
        View=ifft2(Mix)
        View = pg.ImageItem(View)
        return View  

    def MixingUniMagPhase(self,Image,W1,W2):
        self.setMagnitude()
        self.setPhase()
        Image.setMagnitude()
        Image.setPhase()
        UniTemp=Image.getMagnitude()
        for i in range (len(UniTemp)):
            UniTemp[i]=1
        TempMagnitude=list(map(add, ((W1)*(np.array(UniTemp))),((1-W1)*(np.array(Image.getMagnitude())))) )
        TempPhase=np.exp(list(map(add, ((W2)*(np.array(Image.getPhase()))), ((1-W2)*(np.array(self.getPhase())))) ))
        Mix=[a*b for a,b in zip(TempMagnitude,TempPhase)]
        View=ifft2(Mix)
        View = pg.ImageItem(View)
        return View       

    def MixingUniMagUniPhase(self,Image,W1,W2):
        self.setMagnitude()
        self.setPhase()
        Image.setMagnitude()
        Image.setPhase()
        UniTempMag=self.ImageObject.getMagnitude()
        UniTempPhase=Image.getPhase()
        for i in range (len(UniTempMag)):
            UniTempMag[i]=1
            UniTempPhase[i]=0
        TempMagnitude=list(map(add, ((W1)*(np.array(UniTempMag))),((1-W1)*(np.array(Image.getMagnitude())))) )
        TempPhase=np.exp(list(map(add, ((W2)*(np.array(UniTempPhase))), ((1-W2)*(np.array(self.getPhase())))) ))
        Mix=[a*b for a,b in zip(TempMagnitude,TempPhase)]
        View=ifft2(Mix)
        View = pg.ImageItem(View)
        return View

    def MixingRealImaginary(self,Image,W1,W2):
        self.setReal()
        self.setImaginary()
        Image.setReal()
        Image.setImaginary()
        TempReal =list(map(add, ((W1) * np.array((self.ImageObject.getReal()))), ((1-W1) * np.array(Image.getReal()))) ) 
        TempImag =list(map(add, ((W2) * np.array((Image.getImaginary()))), ((1-W2) * np.array((self.ImageObject.getImaginary())))) ) 
        CompleteMix=[]
        for i in (len(self.ImageObject)):
            CompleteMix.append(complex(TempReal[i],TempImag[i]))
        View=ifft2(ComplexMix)
        View = pg.ImageItem(View)
        return View

    def setMagnitude(self):
        MagnitudeTemp=self.ImageObject
        FFT2D = fft2(MagnitudeTemp)
        self.Magnitude=(np.abs(FFT2D))
    def setPhase(self):
        PhaseTemp=self.ImageObject
        FFT2D = fft2(PhaseTemp)
        self.Phase=np.angle(FFT2D)

    def setReal(self):
        RealTemp=self.ImageObject
        FFT2D = fft2(RealTemp)
        self.Real=np.real(FFT2D)

    def setImaginary(self):
        ImagTemp=self.ImageObject
        FFT2D = fft2(ImagTemp)
        self.Imaginary=np.real(FFT2D)

    def getMagnitude(self):
        return self.Magnitude
    def getPhase(self):
        return self.Phase
    def getReal(self):
        return self.Real
    def getImaginary(self):
        return self.Imaginary
    def getImage(self):
        return self.ImageObject    

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1596, 917)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.Image1ComboBox = QtWidgets.QComboBox(self.centralwidget)
        self.Image1ComboBox.setObjectName("Image1ComboBox")
        self.gridLayout.addWidget(self.Image1ComboBox, 0, 1, 1, 1)
        self.Browse1 = QtWidgets.QPushButton(self.centralwidget)
        self.Browse1.setObjectName("Browse1")
        self.gridLayout.addWidget(self.Browse1, 0, 0, 1, 1)
        self.Image1Display = PlotWidget(self.centralwidget)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.NoBrush)
        self.Image1Display.setBackgroundBrush(brush)
        self.Image1Display.setObjectName("Image1Display")
        self.gridLayout.addWidget(self.Image1Display, 1, 0, 1, 1)
        self.Image1Change = PlotWidget(self.centralwidget)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.NoBrush)
        self.Image1Change.setBackgroundBrush(brush)
        self.Image1Change.setObjectName("Image1Change")
        self.gridLayout.addWidget(self.Image1Change, 1, 1, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.gridLayout_4 = QtWidgets.QGridLayout()
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("cmr10")
        font.setPointSize(14)
        self.label_9.setFont(font)
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_3.addWidget(self.label_9)
        self.MixerChoose = QtWidgets.QComboBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.MixerChoose.sizePolicy().hasHeightForWidth())
        self.MixerChoose.setSizePolicy(sizePolicy)
        self.MixerChoose.setObjectName("MixerChoose")
        self.horizontalLayout_3.addWidget(self.MixerChoose)
        self.gridLayout_4.addLayout(self.horizontalLayout_3, 0, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("cmr10")
        font.setPointSize(14)
        self.label_10.setFont(font)
        self.label_10.setAlignment(QtCore.Qt.AlignCenter)
        self.label_10.setObjectName("label_10")
        self.horizontalLayout.addWidget(self.label_10)
        self.ImageChoose1 = QtWidgets.QComboBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ImageChoose1.sizePolicy().hasHeightForWidth())
        self.ImageChoose1.setSizePolicy(sizePolicy)
        self.ImageChoose1.setObjectName("ImageChoose1")
        self.horizontalLayout.addWidget(self.ImageChoose1)
        self.Slider1 = QtWidgets.QSlider(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Slider1.sizePolicy().hasHeightForWidth())
        self.Slider1.setSizePolicy(sizePolicy)
        self.Slider1.setMaximum(100)
        self.Slider1.setOrientation(QtCore.Qt.Horizontal)
        self.Slider1.setObjectName("Slider1")
        self.horizontalLayout.addWidget(self.Slider1)
        self.SliderValue1 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SliderValue1.sizePolicy().hasHeightForWidth())
        self.SliderValue1.setSizePolicy(sizePolicy)
        self.SliderValue1.setText("")
        self.SliderValue1.setObjectName("SliderValue1")
        self.horizontalLayout.addWidget(self.SliderValue1)
        self.gridLayout_4.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        self.Component1ComboBox = QtWidgets.QComboBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Component1ComboBox.sizePolicy().hasHeightForWidth())
        self.Component1ComboBox.setSizePolicy(sizePolicy)
        self.Component1ComboBox.setObjectName("Component1ComboBox")
        self.gridLayout_4.addWidget(self.Component1ComboBox, 2, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_11 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_11.sizePolicy().hasHeightForWidth())
        self.label_11.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("cmr10")
        font.setPointSize(14)
        self.label_11.setFont(font)
        self.label_11.setAlignment(QtCore.Qt.AlignCenter)
        self.label_11.setObjectName("label_11")
        self.horizontalLayout_2.addWidget(self.label_11)
        self.ImageChoose2 = QtWidgets.QComboBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ImageChoose2.sizePolicy().hasHeightForWidth())
        self.ImageChoose2.setSizePolicy(sizePolicy)
        self.ImageChoose2.setObjectName("ImageChoose2")
        self.horizontalLayout_2.addWidget(self.ImageChoose2)
        self.Slider2 = QtWidgets.QSlider(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Slider2.sizePolicy().hasHeightForWidth())
        self.Slider2.setSizePolicy(sizePolicy)
        self.Slider2.setMaximum(100)
        self.Slider2.setOrientation(QtCore.Qt.Horizontal)
        self.Slider2.setObjectName("Slider2")
        self.horizontalLayout_2.addWidget(self.Slider2)
        self.SliderValue2 = QtWidgets.QLabel(self.centralwidget)
        self.SliderValue2.setText("")
        self.SliderValue2.setObjectName("SliderValue2")
        self.horizontalLayout_2.addWidget(self.SliderValue2)
        self.gridLayout_4.addLayout(self.horizontalLayout_2, 3, 0, 1, 1)
        self.Component2ComboBox = QtWidgets.QComboBox(self.centralwidget)
        self.Component2ComboBox.setObjectName("Component2ComboBox")
        self.gridLayout_4.addWidget(self.Component2ComboBox, 4, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout_4, 0, 1, 1, 1)
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.Browse2 = QtWidgets.QPushButton(self.centralwidget)
        self.Browse2.setObjectName("Browse2")
        self.gridLayout_3.addWidget(self.Browse2, 0, 0, 1, 1)
        self.Image2ComboBox = QtWidgets.QComboBox(self.centralwidget)
        self.Image2ComboBox.setObjectName("Image2ComboBox")
        self.gridLayout_3.addWidget(self.Image2ComboBox, 0, 1, 1, 1)
        self.Image2Display = PlotWidget(self.centralwidget)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.NoBrush)
        self.Image2Display.setBackgroundBrush(brush)
        self.Image2Display.setObjectName("Image2Display")
        self.gridLayout_3.addWidget(self.Image2Display, 1, 0, 1, 1)
        self.Image2Change = PlotWidget(self.centralwidget)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.NoBrush)
        self.Image2Change.setBackgroundBrush(brush)
        self.Image2Change.setObjectName("Image2Change")
        self.gridLayout_3.addWidget(self.Image2Change, 1, 1, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout_3, 1, 0, 1, 1)
        self.gridLayout_5 = QtWidgets.QGridLayout()
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.IgnoreLabel1 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.IgnoreLabel1.sizePolicy().hasHeightForWidth())
        self.IgnoreLabel1.setSizePolicy(sizePolicy)
        self.IgnoreLabel1.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.IgnoreLabel1.setAlignment(QtCore.Qt.AlignCenter)
        self.IgnoreLabel1.setObjectName("IgnoreLabel1")
        self.gridLayout_5.addWidget(self.IgnoreLabel1, 0, 0, 1, 1)
        self.IgnoreLabel2 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.IgnoreLabel2.sizePolicy().hasHeightForWidth())
        self.IgnoreLabel2.setSizePolicy(sizePolicy)
        self.IgnoreLabel2.setAlignment(QtCore.Qt.AlignCenter)
        self.IgnoreLabel2.setObjectName("IgnoreLabel2")
        self.gridLayout_5.addWidget(self.IgnoreLabel2, 0, 1, 1, 1)
        self.Output1Image = PlotWidget(self.centralwidget)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.NoBrush)
        self.Output1Image.setBackgroundBrush(brush)
        self.Output1Image.setObjectName("Output1Image")
        self.gridLayout_5.addWidget(self.Output1Image, 1, 0, 1, 1)
        self.Output2Image = PlotWidget(self.centralwidget)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.NoBrush)
        self.Output2Image.setBackgroundBrush(brush)
        self.Output2Image.setObjectName("Output2Image")
        self.gridLayout_5.addWidget(self.Output2Image, 1, 1, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout_5, 1, 1, 1, 1)
        self.SizeError = QtWidgets.QLabel(self.centralwidget)
        self.SizeError.setObjectName("SizeError")
        self.gridLayout_2.addWidget(self.SizeError, 2, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1596, 25))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        FourierArr=["Mag,Phase,Real,Imag","Magnitude","Phase","Real","Imaginary"]
        self.Image2ComboBox.addItems(FourierArr)
        self.Image1ComboBox.addItems(FourierArr)
        OutputCount=["Output1,Output2","Output1","Output2"]
        self.MixerChoose.addItems(OutputCount)
        self.FourierPlusArr=["Mag,Phase,Real,Imag,uniMag,uniPhase","Magnitude","Phase","Real","Imaginary","UniMagnitude","UniPhase"]
        self.Component1ComboBox.addItems(self.FourierPlusArr)
        self.Component2ComboBox.addItems(self.FourierPlusArr)
        ImageCount=["Img1,Img2","Image1","Image2"]
        self.ImageChoose1.addItems(ImageCount)
        self.ImageChoose2.addItems(ImageCount)

        self.ImageDisplayArr=[self.Image1Display , self.Image2Display]
        self.SimpleComboBoxArr=[self.Image1ComboBox ,self.Image2ComboBox]
        self.SimpleGraphicsViewArr=[self.Image1Change , self.Image2Change]
        self.ComplexComboBoxArr=[self.Component1ComboBox , self.Component2ComboBox]
        self.ImageChooseArr=[self.ImageChoose1 , self.ImageChoose2]
        self.PhaseArr=["Phase , UniPhase","Phase","UniPhase"]
        self.MagnitudeArr=["Magnitude , UniMagnitude","Magnitude","UniMagnitude"]
        self.ChooseRealArr=["Choose...","Real"]
        self.ChooseImaginaryArr=["Choose...","Imaginary"]
        self.IMG1=Image()
        self.IMG2=Image()
        self.ImageArr=[self.IMG1 ,self.IMG2]
        self.OutputArr=[self.Output1Image , self.Output2Image]
        self.SliderArr=[self.Slider1 , self.Slider2]
        self.LabelArr=[self.SliderValue1 , self.SliderValue2]

        self.Image1ComboBox.setEnabled(False)
        self.Image2ComboBox.setEnabled(False)
        self.MixerChoose.setEnabled(False)
        self.ImageChoose1.setEnabled(False)
        self.ImageChoose2.setEnabled(False)
        self.Component1ComboBox.setEnabled(False)
        self.Component2ComboBox.setEnabled(False)
        self.Slider1.setEnabled(False)
        self.Slider2.setEnabled(False)


        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.Browse1.setText(_translate("MainWindow", "Insert Image"))
        self.label_9.setText(_translate("MainWindow", "Mixer Output to"))
        self.label_10.setText(_translate("MainWindow", "Component1"))
        self.SliderValue1.setText(_translate("MainWindow", "%"))
        self.label_11.setText(_translate("MainWindow", "Component2"))
        self.SliderValue2.setText(_translate("MainWindow", "%"))
        self.Browse2.setText(_translate("MainWindow", "Insert Image"))
        self.IgnoreLabel1.setText(_translate("MainWindow", "Output1"))
        self.IgnoreLabel2.setText(_translate("MainWindow", "Output2"))
        self.SizeError.setText(_translate("MainWindow", " "))
        self.Browse1.clicked.connect(lambda:self.InsertImage(0))
        self.Browse2.clicked.connect(lambda:self.InsertImage(1))
        self.Image1ComboBox.activated.connect(lambda:self.ImageComponent(0))
        self.Image2ComboBox.activated.connect(lambda:self.ImageComponent(1))
        self.Component1ComboBox.activated.connect(lambda:self.ManageComboBox(0,1))
        self.Component2ComboBox.activated.connect(lambda:self.ManageComboBox(1,0))
        self.Slider1.valueChanged.connect(lambda:self.SliderDetector(0))
        self.Slider2.valueChanged.connect(lambda:self.SliderDetector(1))
        self.MixerChoose.activated.connect(self.ManageMixing)
        self.ImageChoose1.activated.connect(self.ManageMixing)
        self.ImageChoose2.activated.connect(self.ManageMixing)
        self.Component1ComboBox.activated.connect(self.ManageMixing)
        self.Component2ComboBox.activated.connect(self.ManageMixing)


    def InsertImage(self,i):
        filename=QtWidgets.QFileDialog.getOpenFileName()
        directory=filename[0]
        self.SizeError.setText(" ")
        self.ImageArr[i].SetImage(directory)
        if(self.IMG1.CheckEmpty() or self.IMG2.CheckEmpty()):
            self.SimpleComboBoxArr[i].setEnabled(True)
            self.ImageDisplayArr[i].addItem(self.ImageArr[i].DisplayImage())
            logging.info('Image:{} is added'.format(i+1))
        else:
            if((self.IMG1.CheckEqual(self.IMG2))):
                self.SimpleComboBoxArr[i].setEnabled(True)
                self.MixerChoose.setEnabled(True)
                self.ImageChoose1.setEnabled(True)
                self.ImageChoose2.setEnabled(True)
                self.Component1ComboBox.setEnabled(True)
                self.Component2ComboBox.setEnabled(True)
                self.Slider1.setEnabled(True)
                self.Slider2.setEnabled(True)
                self.ImageDisplayArr[i].addItem(self.ImageArr[i].DisplayImage())
                logging.info('Image:{} is added'.format(i+1))
            else:
                self.ImageArr[i].EmptyImage()
                self.SizeError.setText("     SIZE ERROR!!! insert image of the same size")
                self.SizeError.setStyleSheet('color: red')
                logging.error('the user did not insert image of the same size ')


                
    def SliderDetector(self, i):
        val=self.SliderArr[i].value()
        self.LabelArr[i].setText(str(val) + "%")        
        


    def ImageComponent(self,i):
        if(self.SimpleComboBoxArr[i].currentIndex() == 1 ):
            self.SimpleGraphicsViewArr[i].addItem(self.ImageArr[i].DisplayImageMag())
            logging.info('the user choose Magnitude to view of image {} '.format(i+1))
        elif(self.SimpleComboBoxArr[i].currentIndex() == 2 ):
            self.SimpleGraphicsViewArr[i].addItem(self.ImageArr[i].DisplayImagePhase())
            logging.info('the user choose Phase to view of image {} '.format(i+1))
        elif(self.SimpleComboBoxArr[i].currentIndex() == 3 ):
            self.SimpleGraphicsViewArr[i].addItem(self.ImageArr[i].DisplayImageReal())
            logging.info('the user choose Real to view of image {} '.format(i+1))
        elif(self.SimpleComboBoxArr[i].currentIndex() == 4 ):
            self.SimpleGraphicsViewArr[i].addItem(self.ImageArr[i].DisplayImageImag())
            logging.info('the user choose Imaginary to view of image {} '.format(i+1))
        
    


    def ManageMixing(self):
        if((self.ImageChooseArr[0].currentIndex() == 0 or self.ImageChooseArr[1].currentIndex() == 0) or (self.ComplexComboBoxArr[0].currentIndex() == 0 or self.ComplexComboBoxArr[1].currentIndex() == 0) or (self.MixerChoose.currentIndex() == 0) ):
            pass
        else :
            if (self.MixerChoose.currentIndex() == 1):
                if((self.ImageChoose1.currentIndex() == 1 and self.ImageChoose2.currentIndex() == 2)):
                    self.ChooseMixer(0,0,1)
                elif((self.ImageChoose1.currentIndex() == 2 and self.ImageChoose2.currentIndex() == 1)):
                    self.ChooseMixer(0,1,0)
                elif((self.ImageChoose1.currentIndex() == 1 and self.ImageChoose2.currentIndex() == 1)):
                    self.ChooseMixer(0,0,0)
                elif((self.ImageChoose1.currentIndex() == 2 and self.ImageChoose2.currentIndex() == 2)):
                    self.ChooseMixer(0,1,1)
            elif (self.MixerChoose.currentIndex() == 2):
                if((self.ImageChoose1.currentIndex() == 1 and self.ImageChoose2.currentIndex() == 2)):
                    self.ChooseMixer(1,0,1)
                elif((self.ImageChoose1.currentIndex() == 2 and self.ImageChoose2.currentIndex() == 1)):
                    self.ChooseMixer(1,1,0)
                elif((self.ImageChoose1.currentIndex() == 1 and self.ImageChoose2.currentIndex() == 1)):
                    self.ChooseMixer(1,0,0)
                elif((self.ImageChoose1.currentIndex() == 2 and self.ImageChoose2.currentIndex() == 2)):
                    self.ChooseMixer(1,1,1)
           

                                    


    def ManageComboBox(self,i1,i2):
        if(self.ComplexComboBoxArr[i1].currentIndex() == 0 ):
            self.ComplexComboBoxArr[i1].clear()
            self.ComplexComboBoxArr[i1].addItems(self.FourierPlusArr)
            self.ComplexComboBoxArr[i2].clear()
            self.ComplexComboBoxArr[i2].addItems(self.FourierPlusArr)
            logging.info('the user returned the two combobox to their intial state')
        else:
            if(self.ComplexComboBoxArr[i2].currentIndex() == 0 or self.ComplexComboBoxArr[i2].count() < 7 ):
                if(self.ComplexComboBoxArr[i1].currentIndex() == 1  or self.ComplexComboBoxArr[i1].currentIndex() == 5 ):
                    self.ComplexComboBoxArr[i2].clear()
                    self.ComplexComboBoxArr[i2].addItems(self.PhaseArr)
                    # logging.info('the user choose Magnitude/UniMagnitue of image {} to mix with Phase/UniPhase of image {}'.format(i1+1,i2+1))    
                elif(self.ComplexComboBoxArr[i1].currentIndex() == 2 or self.ComplexComboBoxArr[i1].currentIndex() == 6 ):
                    self.ComplexComboBoxArr[i2].clear()
                    self.ComplexComboBoxArr[i2].addItems(self.MagnitudeArr)
                    # logging.info('the user choose Phase/UniPhase of image {} to mix with Magnitude/UniMagnitue of image {}'.format(i1+1,i2+1))
                elif(self.ComplexComboBoxArr[i1].currentIndex() == 3 ):
                    self.ComplexComboBoxArr[i2].clear()
                    self.ComplexComboBoxArr[i2].addItems(self.ChooseImaginaryArr)
                    # logging.info('the user choose the real part of image {} to mix with the imaginary part of image {}'.format(i1+1,i2+1))
                elif(self.ComplexComboBoxArr[i1].currentIndex() == 4 ):
                    self.ComplexComboBoxArr[i2].clear()
                    self.ComplexComboBoxArr[i2].addItems(self.ChooseRealArr)
                    # logging.info('the user choose the imaginary part of image {} to mix with the real part of image {}'.format(i1+1,i2+1))
       



    def ChooseMixer(self,i,i1,i2):
        W1=self.Slider1.value()
        W2=self.Slider2.value()
        W1=(W1/100)
        W2=(W2/100)  
        ViewValue=pg.ImageItem()
        if(str(self.Component1ComboBox.currentText()) == "Magnitude"):
            if(str(self.Component2ComboBox.currentText()) == "Phase"):
                ViewValue=self.ImageArr[i1].MixingMagPhase(self.ImageArr[i2],W1,W2)
                logging.info('the user choose to mix {} %, of the magnitude of image {} with {} %, of the phase of image {}'.format(W1*100,i1+1,W2*100,i2+1))
            elif(str(self.Component1ComboBox.currentText()) == "UniPhase"):
                ViewValue=self.ImageArr[i1].MixingMagPhase(self.ImageArr[i2],W1,W2)
                logging.info('the user choose to mix {} %, of the magnitude of image {} with {} %, of the uniphase of image {}'.format(W1*100,i1+1,W2*100,i2+1))
        elif(str(self.Component1ComboBox.currentText()) == "Phase"):
            if(str(self.Component2ComboBox.currentText()) == "Magnitude"):
                ViewValue=self.ImageArr[i2].MixingMagPhase(self.ImageArr[i1],W2,W1)
                logging.info('the user choose to mix {} %, of the phase of image {} with {} %, of the magnitude of image {}'.format(W1*100,i1+1,W2*100,i2+1))
            elif(str(self.Component1ComboBox.currentText()) == "UniMagnitude"):
                ViewValue=self.ImageArr[i2].MixingMagPhase(self.ImageArr[i1],W2,W1)
                logging.info('the user choose to mix {} %, of the phase of image {} with {} %, of the unimagnitude of image {}'.format(W1*100,i1+1,W2*100,i2+1))
        elif(str(self.Component1ComboBox.currentText()) == "UniMagnitude"):
            if(str(self.Component2ComboBox.currentText()) == "Phase"):
               ViewValue=self.ImageArr[i1].MixingMagPhase(self.ImageArr[i2],W1,W2)
               logging.info('the user choose to mix {} %, of the unimagnitude of image {} with {} %, of the phase of image {}'.format(W1*100,i1+1,W2*100,i2+1))
            elif(str(self.Component1ComboBox.currentText()) == "UniPhase"):
                ViewValue=self.ImageArr[i1].MixingMagPhase(self.ImageArr[i2],W1,W2)
                logging.info('the user choose to mix {} %, of the unimagnitude of image {} with {} %, of the uniphase of image {}'.format(W1*100,i1+1,W2*100,i2+1))
        elif(str(self.Component1ComboBox.currentText()) == "UniPhase"):
            if(str(self.Component2ComboBox.currentText()) == "Magnitude"):
                ViewValue=self.ImageArr[i2].MixingMagPhase(self.ImageArr[i1],W2,W1)
                logging.info('the user choose to mix {} %, of the uniphase of image {} with {} %, of the magnitude of image {}'.format(W1*100,i1+1,W2*100,i2+1))
            elif(str(self.Component1ComboBox.currentText()) == "UniMagnitude"):
                ViewValue=self.ImageArr[i2].MixingMagPhase(self.ImageArr[i1],W2,W1)
                logging.info('the user choose to mix {} %, of the uniphase of image {} with {} %, of the unimagnitude of image {}'.format(W1*100,i1+1,W2*100,i2+1))
        elif(str(self.Component1ComboBox.currentText()) == "Real"):
            ViewValue=self.ImageArr[i1].MixingMagPhase(self.ImageArr[i2],W1,W2)
            logging.info('the user choose to mix {} %, of the real part of image {} with {} %, of the imaginary part of image {}'.format(W1*100,i1+1,W2*100,i2+1))
        elif(str(self.Component1ComboBox.currentText()) == "Imaginary"):
            ViewValue=self.ImageArr[i2].MixingMagPhase(self.ImageArr[i1],W2,W1)
            logging.info('the user choose to mix {} %, of the imaginary part of image {} with {} %, of the real part of image {}'.format(W1*100,i1+1,W2*100,i2+1))
        self.OutputArr[i].addItem(ViewValue)
        logging.info('output displayed in output {} port '.format(i+1))
            
            