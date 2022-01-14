# embedding_in_qt5.py --- Simple Qt5 application embedding matplotlib canvases
#
# Copyright (C) 2005 Florent Rougon
#               2006 Darren Dale
#               2015 Jens H Nielsen
# Modified by Peter Mackenzie-Helnwein on Dec 6, 2018
#
# This file is an example program for matplotlib. It may be used and
# modified with no restriction; raw copies as well as modified versions
# may be distributed without limitation.

# MODIFIED BY YASHAR ZAFARI FOR CESG 505 FINAL

import sys
import numpy as np

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QMenu, \
                            QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,\
                            QSizePolicy, QPushButton, QMessageBox, QComboBox,\
                            QButtonGroup, QCheckBox, QDialog, QDoubleSpinBox

from PyQt5 import QtCore
from PyQt5.QtCore import Qt
import matplotlib
# Make sure that we are using QT5
matplotlib.use('Qt5Agg')

from numpy import arange, sin, cos, pi, linspace, zeros
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


## define a systemplot class

class MyBeamMplCanvas(FigureCanvas):
    """Simple canvas with a sine plot."""

    def __init__(self, parent=None, **kwargs):
        self.L = 1.0
        self.leftBC = 1
        self.rightBC = 1
        self.W = 1.0
        self.E = 29000.0
        self.I = 100.0
        self.output = 0

        self.fig = Figure()
        self.axes = self.fig.add_subplot(211)
        self.axes2 = self.fig.add_subplot(212, sharex = self.axes)

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        self.refresh()

    def setLength(self, L):
        self.L = L
        self.refresh()

    def setE(self, E):
        self.E = E
        self.refresh()

    def setW(self, W):
        self.W = W
        self.refresh()

    def setI(self, I):
        self.I = I
        self.refresh()

    def setLBC(self, l):
        self.leftBC = l
        self.refresh()

    def setRBC(self, l):
        self.rightBC = l
        self.refresh()

    def setOutput(self, o):
        self.output = o
        self.refresh()

    def refresh(self):

        # clean up old plots

        self.axes.cla()
        self.axes2.cla()

        d = self.L / 20.

        # plot the beam (undeformed)

        t = linspace(0.0, self.L, 20)
        s = zeros(20)
        self.axes.plot(t, s, '-k')

        # plot the support conditions

        if self.leftBC == 1 and self.rightBC == 1:                  # draw pin-pin condition
            x1 = [0, d, -d, 0]
            y1 = [0, -d, -d ,0]
            x2 = [self.L, self.L+d, self.L-d, self.L]
            y2 = [0, -d, -d ,0]
            self.axes.plot(x1, y1, '-b')
            self.axes.plot(x2, y2, '-b')

        elif self.leftBC == 2 and self.rightBC == 0:                # draw fixed-free condition
            self.axes.plot([0,0], [+d,-d], '-b')

        elif self.leftBC == 0 and self.rightBC == 2:                # draw free-fixed condition
            self.axes.plot([self.L, self.L], [+d, -d], '-b')

        elif self.leftBC == 2 and self.rightBC == 2:                # draw fixed fixed condition
            self.axes.plot([0, 0], [+d, -d], '-b')
            self.axes.plot([self.L, self.L], [+d, -d], '-b')

        elif self.leftBC == 2 and self.rightBC == 1:                # draw fixed-pin condition
            self.axes.plot([0, 0], [+d, -d], '-b')
            x2 = [self.L, self.L + d, self.L - d, self.L]
            y2 = [0, -d, -d, 0]
            self.axes.plot(x2, y2, '-b')

        elif self.leftBC == 1 and self.rightBC == 2:                # draw pin-fixed condition
            x1 = [0, d, -d, 0]
            y1 = [0, -d, -d, 0]
            self.axes.plot(x1, y1, '-b')
            self.axes.plot([self.L, self.L], [+d, -d], '-b')

        # plot deformed beam (just some fantasy function here
        x = np.linspace(0, self.L)
        # deflection plots
        # fix - free
        if self.leftBC == 2 and self.rightBC == 0 and self.output == 0:
            y = (-(self.W * x**2 / (24 * self.E * self.I)) * (6 * self.L**2 - 4 * self.L * x + x**2))
        # free - fix
        elif self.leftBC == 0 and self.rightBC == 2 and self.output == 0:
            y = (-(self.W / (24 * self.E * self.I)) * (x**4 - 4 * self.L**3 * x + 3 * self.L**4))
        # fix - fix
        elif self.leftBC == 2 and self.rightBC == 2 and self.output == 0:
            y = (-(self.W * x**2 / (24 * self.E * self.I)) * (self.L - x)**2)
        # pin - pin
        elif self.leftBC == 1 and self.rightBC == 1 and self.output == 0:
            y = (-(self.W * x / (24 * self.E * self.I)) * (self.L**3 - 2 * self.L * x**2 + x**3))
        # pin - fix
        elif self.leftBC == 1 and self.rightBC == 2 and self.output == 0:
            y = (-(self.W * x / (48 * self.E * self.I)) * (self.L**3 - 3 * self.L * x**2 + 2 * x**3))
        # fix - pin
        elif self.leftBC == 2 and self.rightBC == 1 and self.output == 0:
            y = ((self.W * (x - self.L) / (48 * self.E * self.I)) * (self.L**3 - 3 * self.L * (x - self.L)**2 - \
                                                                   2 * (x - self.L)**3))
        # rotation plots
        # fix - free
        elif self.leftBC == 2 and self.rightBC == 0 and self.output == 1:
            y = (-(self.W * x / (6 * self.E * self.I)) * (3 * self.L**2 - 3 * self.L * x + x**2))
        # free - fix
        elif self.leftBC == 0 and self.rightBC == 2 and self.output == 1:
            y = ((self.W * (x-self.L) / (6 * self.E * self.I)) * (3 * self.L**2 - 3 * self.L * -(x-self.L) + \
                                                                          (x-self.L)**2))
        # fix - fix
        elif self.leftBC == 2 and self.rightBC == 2 and self.output == 1:
            y = (-(self.W * x * (self.L**2 - 3 * self.L * x + 2 * x**2)) / (12 * self.E * self.I))
        # pin - pin
        elif self.leftBC == 1 and self.rightBC == 1 and self.output == 1:
            y = (-(self.W * (self.L**3 - 6 * self.L * x**2 + 4 * x**3)) / (24 * self.E * self.I))
        # pin - fix
        elif self.leftBC == 1 and self.rightBC == 2 and self.output == 1:
            y = (-(self.W * (self.L**3 - 9 * self.L * x**2 + 8 * x**3)) / (48 * self.E * self.I))
        # fix - pin
        elif self.leftBC == 2 and self.rightBC == 1 and self.output == 1:
            y = (-(self.W * x ) * (6 * self.L**2 - 15 * self.L * x + 8 * x**2) / (48 * self.E * self.I))

        # shear plots
        # fix - free
        elif self.leftBC == 2 and self.rightBC == 0 and self.output == 2:
            y = self.W * (self.L - x)
        # free - fix
        elif self.leftBC == 0 and self.rightBC == 2 and self.output == 2:
            y = self.W * x
        # fix - fix
        elif self.leftBC == 2 and self.rightBC == 2 and self.output == 2:
            y = self.W * (self.L / 2 - x)
        # pin - pin
        elif self.leftBC == 1 and self.rightBC == 1 and self.output == 2:
            y = self.W * (self.L / 2 - x)
        # pin - fix
        elif self.leftBC == 1 and self.rightBC == 2 and self.output == 2:
            y = ((3 * self.W * self.L / 8) - (self.W * x))
        # fix - pin
        elif self.leftBC == 2 and self.rightBC == 1 and self.output == 2:
            y = ((5 * self.W * self.L / 8) - (self.W * x))

        # moment plots
        # fix - free
        elif self.leftBC == 2 and self.rightBC == 0 and self.output == 3:
            y = (-self.W * (self.L - x) ** 2) / 2
        # free - fix
        elif self.leftBC == 0 and self.rightBC == 2 and self.output == 3:
            y = (-self.W * x**2) / 2
        # fix - fix
        elif self.leftBC == 2 and self.rightBC == 2 and self.output == 3:
            y = (self.W / 12) * (6 * self.L * x - 6 * x**2 - self.L**2)
        # pin - pin
        elif self.leftBC == 1 and self.rightBC == 1 and self.output == 3:
            y = (self.W * x / 2) * (self.L - x)
        # pin - fix
        elif self.leftBC == 1 and self.rightBC == 2 and self.output == 3:
            y = (((3 * self.W * self.L / 8) * x) - (self.W * x**2 / 2))
        # fix - pin
        elif self.leftBC == 2 and self.rightBC == 1 and self.output == 3:
            y = (((3 * self.W * self.L / 8) * -(x - self.L)) - (self.W * (x - self.L)**2 / 2))

        # for the unstable conditions, draw line at 0
        else:
            y = 0 * x

        self.axes2.plot(x,y, '-r')

        self.axes.axis('equal')
        #self.axes2.axis('equal')

        self.draw()

## define the application class

class ApplicationWindow(QMainWindow):
    def __init__(self):
        # Menu options for main window
        QMainWindow.__init__(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle("Beam Calculator")

        self.file_menu = QMenu('&File', self)
        self.file_menu.addAction('&Quit', self.fileQuit,
                                 QtCore.Qt.CTRL + QtCore.Qt.Key_Q)
        self.file_menu.addAction('&Save', self.saveBtnClicked,
                                 QtCore.Qt.CTRL + QtCore.Qt.Key_S)
        self.menuBar().addMenu(self.file_menu)

        self.help_menu = QMenu('&Help', self)
        self.menuBar().addSeparator()
        self.menuBar().addMenu(self.help_menu)

        self.help_menu.addAction('&About', self.about)

        self.main_widget = QWidget(self)

        l = QVBoxLayout(self.main_widget)
        self.systemplot = MyBeamMplCanvas(self.main_widget)
        self.systemplot.setLength(10.)
        self.systemplot.setLBC(1)
        self.systemplot.setRBC(1)
        self.systemplot.setW(1.0)
        self.systemplot.setE(29000.0)
        self.systemplot.setI(21.33)
        self.systemplot.setOutput(0)

        # buttons for different boundary conditions
        btn_clamp_L = QPushButton('Fix',self.main_widget)
        btn_clamp_L.clicked.connect(self.onLBtnClampedClicked)

        btn_pinned_L = QPushButton('Pin',self.main_widget)
        btn_pinned_L.clicked.connect(self.onLBtnPinnedClicked)

        btn_free_L = QPushButton('Free',self.main_widget)
        btn_free_L.clicked.connect(self.onLBtnFreeClicked)

        btn_clamp_R = QPushButton('Fix', self.main_widget)
        btn_clamp_R.clicked.connect(self.onRBtnClampedClicked)

        btn_pinned_R = QPushButton('Pin', self.main_widget)
        btn_pinned_R.clicked.connect(self.onRBtnPinnedClicked)

        btn_free_R = QPushButton('Free', self.main_widget)
        btn_free_R.clicked.connect(self.onRBtnFreeClicked)

        # put boundary condition buttons together
        lytl = QVBoxLayout()
        lytl.addWidget(btn_free_L)
        lytl.addWidget(btn_pinned_L)
        lytl.addWidget(btn_clamp_L)
        lytr = QVBoxLayout()
        lytr.addWidget(btn_free_R)
        lytr.addWidget(btn_pinned_R)
        lytr.addWidget(btn_clamp_R)


        plotlyt = QHBoxLayout()
        plotlyt.addLayout(lytl)
        plotlyt.addWidget(self.systemplot)
        plotlyt.addLayout(lytr)


        # make label and combo box for material selection
        matlbl = QLabel('Select Material:', self)
        self.material = QComboBox(self)
        self.material.addItem('Select Material Type')
        self.material.addItem('Steel (29000 ksi)')
        self.material.addItem('Wood (1900 ksi)')
        self.material.activated[str].connect(self.chooseE)

        lengthlbl = QLabel('Beam Length (in)')
        self.length = QDoubleSpinBox(self)
        self.length.setRange(1., 10000000000000.)
        self.length.setValue(10.)
        self.length.setDecimals(4)
        self.length.valueChanged.connect(self.changeLength)

        # make label and input line for distributed load
        loadlbl = QLabel('Distributed Load (kip/in):', self)
        self.load = QDoubleSpinBox(self)
        self.load.setRange(0., 100000000000000.)
        self.load.setValue(1.)
        self.load.setDecimals(4)
        self.load.valueChanged.connect(self.applyLoad)

        # make label and combo box for section type
        sectlbl = QLabel('Select Section Type', self)
        self.section = QComboBox(self)
        self.section.addItem('Select Section Type')
        self.section.addItem('Rectangle')
        self.section.addItem('I-Beam')
        self.section.activated[str].connect(self.sectionPicked)

        # make a layout that puts together material, load, and section inputs
        lyt2 = QHBoxLayout()
        lyt2.addWidget(matlbl)
        lyt2.addWidget(self.material)
        lyt2.addWidget(lengthlbl)
        lyt2.addWidget(self.length)
        lyt2.addWidget(loadlbl)
        lyt2.addWidget(self.load)
        lyt2.addWidget(sectlbl)
        lyt2.addWidget(self.section)

        # make button group for output results
        outlbl = QLabel('Output Plot:', self)
        # create QButtonGroup
        self.optionbox = QButtonGroup()
        # make check box options
        self.checkd = QCheckBox('Deflection', self.main_widget)
        self.checkt = QCheckBox('Rotation', self.main_widget)
        self.checkv = QCheckBox('Shear', self.main_widget)
        self.checkm = QCheckBox('Moment', self.main_widget)
        # add check boxes to button group
        self.optionbox.addButton(self.checkd)
        self.optionbox.addButton(self.checkt)
        self.optionbox.addButton(self.checkv)
        self.optionbox.addButton(self.checkm)
        # connect to methods to plot desired results
        self.checkd.stateChanged.connect(self.deflectionChecked)
        self.checkt.stateChanged.connect(self.rotationChecked)
        self.checkv.stateChanged.connect(self.shearChecked)
        self.checkm.stateChanged.connect(self.momentChecked)

        # check button layout
        chklyt = QHBoxLayout()
        chklyt.addWidget(outlbl)
        chklyt.addWidget(self.checkd)
        chklyt.addWidget(self.checkt)
        chklyt.addWidget(self.checkv)
        chklyt.addWidget(self.checkm)

        # save figure button
        savebtn = QPushButton('Save Figure', self)
        savebtn.clicked.connect(self.saveBtnClicked)

        # save button layout
        savelyt = QHBoxLayout()
        savelyt.addWidget(savebtn)

        # add all layouts to main layout
        l.addLayout(plotlyt)
        l.addLayout(chklyt)
        l.addLayout(lyt2)
        l.addLayout(savelyt)

        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)

    def onLBtnClampedClicked(self):
        self.systemplot.setLBC(2)

    def onLBtnPinnedClicked(self):
        self.systemplot.setLBC(1)
        if self.systemplot.rightBC == 0:
            warningdlg = errorMessage(self)
            warningdlg.exec()

    def onLBtnFreeClicked(self):
        self.systemplot.setLBC(0)
        if self.systemplot.rightBC == 0 or self.systemplot.rightBC == 1:
            warningdlg = errorMessage(self)
            warningdlg.exec()

    def onRBtnClampedClicked(self):
        self.systemplot.setRBC(2)

    def onRBtnPinnedClicked(self):
        self.systemplot.setRBC(1)
        if self.systemplot.leftBC == 0:
            warningdlg = errorMessage(self)
            warningdlg.exec()

    def onRBtnFreeClicked(self):
        self.systemplot.setRBC(0)
        if self.systemplot.leftBC == 0 or self.systemplot.leftBC == 1:
            warningdlg = errorMessage(self)
            warningdlg.exec()

    def deflectionChecked(self, state):
        if state == Qt.Checked:
            self.systemplot.setOutput(0)

    def rotationChecked(self, state):
        if state == Qt.Checked:
            self.systemplot.setOutput(1)

    def shearChecked(self, state):
        if state == Qt.Checked:
            self.systemplot.setOutput(2)

    def momentChecked(self, state):
        if state == Qt.Checked:
            self.systemplot.setOutput(3)

    def chooseE(self, material):
        if material == 'Wood (1900 ksi)':
            self.systemplot.setE(1900.0)
        elif material == 'Steel (29000 ksi)':
            self.systemplot.setE(29000.0)

    def applyLoad(self, load):
        self.systemplot.setW(load)

    def changeLength(self, length):
        self.systemplot.setLength(length)

    def sectionPicked(self, cursec):
        if cursec == 'Rectangle':
            rectdlg = rectMoI(self)
            rectdlg.exec()
            rI = rectdlg.getRectI()
            self.systemplot.setI(rI)
        elif cursec == 'I-Beam':
            ibeamdlg = ibeamMoI(self)
            ibeamdlg.exec()
            iI = ibeamdlg.getIbeamI()
            self.systemplot.setI(iI)

    def saveBtnClicked(self):
        self.systemplot.fig.savefig('Result Plot.png')

    def fileQuit(self):
        self.close()

    def closeEvent(self, ce):
        self.fileQuit()

    def about(self):
        QMessageBox.about(self, "About",
                                    """ 
                                    Application that analyzes simple beam
                                    by: Yashar Zafari
                                    """
                                )

# Popup window for rectangular moment of inertia
class rectMoI(QDialog):

    def __init__(self, parent = None):
        QDialog.__init__(self, parent)

        # initialize values for width and height
        self.w = 1.0
        self.h = 1.0

        # make window title
        self.setWindowTitle("Moment of Inertia for Rectangular Section")

        # make label and line edit box for width and height
        rwidthlbl = QLabel('Select Section Width:', self)
        rheightlbl = QLabel('Select Section Height:', self)

        # make spin box for selecting values
        rselectw = QDoubleSpinBox(self)
        rselectw.setValue(4.)
        rselectw.valueChanged.connect(self.rgetW)
        rselecth = QDoubleSpinBox(self)
        rselecth.setValue(4.)
        rselecth.valueChanged.connect(self.rgetH)

        # make a push button for when user is done
        rdonebtn = QPushButton('Done', self)
        rdonebtn.clicked.connect(self.close)

        # make layout for width label and entry box
        rwlyt = QHBoxLayout()
        rwlyt.addWidget(rwidthlbl)
        rwlyt.addWidget(rselectw)

        # make layout for height label and entry box
        rhlyt = QHBoxLayout()
        rhlyt.addWidget(rheightlbl)
        rhlyt.addWidget(rselecth)

        # make layout for push button
        rdonelyt = QHBoxLayout()
        rdonelyt.addStretch(1)
        rdonelyt.addWidget(rdonebtn)

        # add all layouts together
        rtotallyt = QVBoxLayout(self)
        rtotallyt.addLayout(rwlyt)
        rtotallyt.addLayout(rhlyt)
        rtotallyt.addLayout(rdonelyt)

        self.setLayout(rtotallyt)

        self.setGeometry(400, 400, 400, 200)

    def rgetW(self, w_value):
        self.w = w_value

    def rgetH(self, h_value):
        self.h = h_value

    def getRectI(self):
        i = self.w * self.h * self.h * self.h / 12
        return i

# Popup window for I-beam moment of inertia
class ibeamMoI(QDialog):

    def __init__(self, parent=None):
        QDialog.__init__(self, parent)

        # initialize values for width, height, and web/flange thickness
        self.w = 1.0
        self.h = 1.0
        self.ft = 0.1
        self.wt = 0.1
        self.lh = 0.8

        # make window title
        self.setWindowTitle("Moment of Inertia for I-Beam Section")

        # make label and line edit box for width, height, and web/flange thickness
        iwidthlbl = QLabel('Select Section Width:', self)
        iheightlbl = QLabel('Select Section Heigh:', self)
        iflangetlbl = QLabel('Select Flange Thickness:', self)
        iwebtlbl = QLabel('Select Web Thickness:', self)

        # make spin box for selecting values
        iselectw = QDoubleSpinBox(self)
        iselectw.valueChanged.connect(self.igetW)
        iselecth = QDoubleSpinBox(self)
        iselecth.valueChanged.connect(self.igetH)
        iselectft = QDoubleSpinBox(self)
        iselectft.valueChanged.connect(self.igetFt)
        iselectwt = QDoubleSpinBox(self)
        iselectwt.valueChanged.connect(self.igetWt)

        # make a push button for when user is done
        idonebtn = QPushButton('Done', self)
        idonebtn.clicked.connect(self.close)

        # make layout for width label and entry box
        iwlyt = QHBoxLayout()
        iwlyt.addWidget(iwidthlbl)
        iwlyt.addWidget(iselectw)

        # make layout for height label and entry box
        ihlyt = QHBoxLayout()
        ihlyt.addWidget(iheightlbl)
        ihlyt.addWidget(iselecth)

        # make layout for flange thickness label and entry box
        iftlyt = QHBoxLayout()
        iftlyt.addWidget(iflangetlbl)
        iftlyt.addWidget(iselectft)

        # make layout for web thickness label and entry box
        iwtlyt = QHBoxLayout()
        iwtlyt.addWidget(iwebtlbl)
        iwtlyt.addWidget(iselectwt)

        # make layout for push button
        idonelyt = QHBoxLayout()
        idonelyt.addStretch(1)
        idonelyt.addWidget(idonebtn)

        # add all layouts together
        itotallyt = QVBoxLayout(self)
        itotallyt.addLayout(iwlyt)
        itotallyt.addLayout(ihlyt)
        itotallyt.addLayout(iftlyt)
        itotallyt.addLayout(iwtlyt)
        itotallyt.addLayout(idonelyt)

        self.setLayout(itotallyt)

        self.setGeometry(400, 400, 400, 200)

    def igetW(self, w_value):
        self.w = w_value

    def igetH(self, h_value):
        self.h = h_value

    def igetFt(self, ft_value):
        self.ft = ft_value

    def igetWt(self, wt_value):
        self.wt = wt_value

    def getIbeamI(self):
        self.lh = self.h - (2 * self.ft)
        i = self.wt * (self.lh ** 3.0) / 12.0
        i += (self.w / 12.0) * ((self.h ** 3) - (self.lh ** 3))
        print(i)
        return i

# Popup window for unstable error message
class errorMessage(QDialog):

    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        warninglbl = QLabel('Warning!!!! Unstable Configuration Picked', self)
        lyt = QVBoxLayout(self)

        closebtn = QPushButton('Ok, I will review my statics')
        closebtn.clicked.connect(self.close)

        lyt.addWidget(warninglbl)
        lyt.addWidget(closebtn)

## the main execution

if __name__ == "__main__":
    qApp = QApplication(sys.argv)
    aw = ApplicationWindow()
    aw.show()
    sys.exit(qApp.exec_())