#!/usr/bin/env python3

import sys
# from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import isoparser
import configparser
# Sample modules for test code
from time import sleep
from os import system

# from PyQt5 import QtWidgets, uic
helptxt = """Select an iso to be installed.
It must contain a system.img for system to be installed.
Make sure the iso is not broken and downloaded correctly.

Install to a specific partition."""

version_name = 'v0.10 Alpha'


class HelpWindow(QWidget):
    def __init__( self ):
        super().__init__()
        self.widget = QWidget(self)
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)
        helptext = QLabel(helptxt)
        helptext.adjustSize( )
        helptext.setFixedWidth(330)
        helptext.setWordWrap(True)
        helptext.setAlignment(Qt.AlignLeft)
        layout.addWidget(helptext)

        self.setWindowTitle('Help')
        self.setGeometry(570, 190, 330, 330)
        self.setFixedWidth(330)
        self.setFixedHeight(330)


class AboutWindow(QWidget):
    def __init__( self ):
        super( ).__init__( )
        self.widget = QWidget(self)
        layout = QVBoxLayout(self)
        layout.addWidget(self.widget)
        pixmap = QPixmap('app/sg_logo.png')
        pixmap = pixmap.scaled(150, 150, Qt.KeepAspectRatio)
        Pixmap_label = QLabel(self)
        Pixmap_label.setPixmap(pixmap)
        Pixmap_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(Pixmap_label)
        # layout.addWidget(pixmap.scaled(100,100,Qt.KeepAspectRatio))

        version_app = QLabel(version_name)
        version_app.setAlignment(Qt.AlignCenter)
        version_app.adjustSize( )

        layout.addWidget(version_app)

        SG_Name = QLabel('Made with time & passion by SupremeGamers')
        SG_Name.setFont(QFont('Arial', 11))

        layout.addWidget(SG_Name)
        layout.addWidget(QLabel(' '))
        author_name = QLabel('Programmed by Jaxparrow')
        author_name.setFont(QFont('Arial', 9))
        author_name.adjustSize( )
        author_name.setAlignment(Qt.AlignCenter)
        layout.addWidget(author_name)
        layout.setAlignment(Qt.AlignCenter)
        self.setWindowTitle('About')
        self.setGeometry(570, 190, 330, 330)
        self.setFixedWidth(330)
        self.setFixedHeight(330)


class Example(QMainWindow):

    def __init__( self, parent=None, frame=QFrame.Box ):
        super( ).__init__( )
        self.initUI( )

    def initUI( self ):
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        # Adding Side Options in Menu

        exitAct = QAction(QIcon('exit.png'), '&Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(qApp.quit)
        self.statusBar( )

        selectiso = QAction(QIcon('exit.png'), '&Select iso', self)
        selectiso.setShortcut('Ctrl+F')
        selectiso.setStatusTip('Select iso file')
        selectiso.triggered.connect(self.openFileNameDialog)
        self.statusBar( )

        AboutAct = QAction(QIcon('exit.png'), '&About', self)
        AboutAct.setShortcut('Ctrl+A')
        AboutAct.setStatusTip('About application')
        AboutAct.triggered.connect(self.OpenAbout)
        self.statusBar( )

        HelpAct = QAction(QIcon('exit.png'), '&Help', self)
        HelpAct.setShortcut('Ctrl+H')
        HelpAct.setStatusTip('Help for  application')
        HelpAct.triggered.connect(self.OpenHelp)
        self.statusBar( )

        self.Isonamevar = 'None'
        self.isExtracting = True

        ##################   Menubar  #############################

        menubar = self.menuBar( )

        # Adding Top Menus
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(selectiso)
        fileMenu.addAction(exitAct)

        helpMenu = menubar.addMenu('&Help')
        helpMenu.addAction(HelpAct)
        helpMenu.addAction(AboutAct)

        ###################   MainUI   #############################

        # Init Base Layout
        mlayout = QVBoxLayout( )
        mlayout.setAlignment(Qt.AlignTop)

        self.Toplayout = QVBoxLayout( )
        self.Toplayout.setAlignment(Qt.AlignTop)

        # Init Top Layout
        self.selectediso = QLabel('Iso : None')
        self.selectediso.setAlignment(Qt.AlignLeft)
        self.OSNAMEtxt = QLineEdit( )
        self.OSVERtxt = QLineEdit( )

        self.InstallationFS = QComboBox()
        self.InstallationFS.addItems(['Ext','OtherFS'])
        self.InstallationFS.currentIndexChanged.connect(self.changemethod)

        self.Datasize = QSlider()
        self.Datasize.setOrientation(Qt.Horizontal)
        self.Datasize.setValue(4)
        self.Datasize.setMaximum(32)
        self.Datasize.setMinimum(4)
        self.Datasize.valueChanged.connect(self.Datachange)
        self.Datasize.setVisible(False)

        self.Datasizetxt = QLabel('Data Image Size: %s GB' % ('4'))
        self.Datasizetxt.setVisible(False)

        self.Installationpart = QComboBox()

        # Rough Code to test.. Will be changed later

        system("grep '/dev/sd' '/proc/mounts' | awk '{print $1;}' > get_part_adv_ins.txt")
        f = open('get_part_adv_ins.txt','r')
        for item in f.read().split():
            self.Installationpart.addItem(item)
        system("rm get_part_adv_ins.txt")

        # End of sample code

        self.Installinglayout = QVBoxLayout()
        self.Installinglayout.setAlignment(Qt.AlignTop)
        self.Installinglayout.addWidget(QLabel('OS Name:'))
        self.Installinglayout.addWidget(self.OSNAMEtxt)
        self.Installinglayout.addWidget(QLabel('OS Version:'))
        self.Installinglayout.addWidget(self.OSVERtxt)

        self.Installingframe = QFrame()
        self.Installingframe.setLayout(self.Installinglayout)
        self.Installingframe.setFrameShadow(QFrame.Raised)
        self.Installingframe.setFrameShape(QFrame.StyledPanel)
        self.Installingframe.setVisible(False)
        self.Installingframe.setFixedHeight(370)


        self.Toplayout.addWidget(self.selectediso)
        self.Toplayout.addWidget(QLabel('Filesystem Type:'))
        self.Toplayout.addWidget(self.InstallationFS)
        self.Toplayout.addWidget(self.Datasizetxt)
        self.Toplayout.addWidget(self.Datasize)
        self.Toplayout.addWidget(QLabel('Installation Partition:'))
        self.Toplayout.addWidget(self.Installationpart)

        Bottomlayout = QVBoxLayout( )
        Bottomlayout.setAlignment(Qt.AlignCenter)
        Bottomlayout.addWidget(QPushButton('Bottom'))

        Bottommenu = QHBoxLayout( )
        Bottommenu.setAlignment(Qt.AlignVCenter)

        self.installprog = QProgressBar( )
        self.installprog.setValue(0)

        # Init Bottom Toolbar
        self.Installbtn = QPushButton('Next')
        self.closebtn = QPushButton('Close')
        self.closebtn.clicked.connect(self.func_quit_all_windows)
        self.Installbtn.setEnabled(False)
        self.Installbtn.clicked.connect(self.Extracting)

        Bottommenu.addWidget(QLabel('            '))
        Bottommenu.addWidget(self.Installbtn)
        Bottommenu.addWidget(self.closebtn)

        self.Bmenuwid = QWidget( )
        self.Bmenuwid.setLayout(Bottommenu)
        self.Bmenuwid.setFixedHeight(60)


        self.rightFrame = QFrame()
        self.rightFrame.setFrameShape(QFrame.StyledPanel)
        self.rightFrame.setFrameShadow(QFrame.Raised)
        self.rightFrame.setLayout(self.Toplayout)
        self.rightFrame.setFixedHeight(370)

        # Adding created widgets
        mlayout.addWidget(self.rightFrame)
        mlayout.addWidget(self.Installingframe)
        mlayout.addWidget(self.installprog)
        mlayout.addWidget(self.Bmenuwid)

        Mainwidget = QWidget( )
        Mainwidget.setLayout(mlayout)
        self.setCentralWidget(Mainwidget)

        ################### Properties ############################

        self.setGeometry(550, 100, 370, 540)
        self.setFixedWidth(370)
        self.setFixedHeight(540)
        self.setWindowTitle('Androidx86 Installer')
        self.show( )


    def changemethod( self ):
        if self.InstallationFS.itemText(self.InstallationFS.currentIndex()) == 'Ext':
            self.Datasize.setVisible(False)
            self.Datasizetxt.setVisible(False)
        else:
            self.Datasize.setVisible(True)
            self.Datasizetxt.setVisible(True)


    def Datachange( self ):
        self.Datasizetxt.setText('Data Image Size: %i GB' % (self.Datasize.value()))

    def Extracting(self):
        if self.isExtracting == True:

            # system("rm iso/*")
            print("Extracting")
            self.Bmenuwid.setEnabled(False)

            # Rough Code to test. Will be changed later
            # system("7z x '%s' -oiso" % (self.Isonamevar))
            # End of test code
            print("Done")

            config = configparser.ConfigParser( )
            config.read('iso/windows/config.ini')

            MetaOSName = config.get('META-DATA', 'NAME')
            MetaOSVer = config.get('META-DATA', 'VERSION')

            if MetaOSName[0] == '"':
                self.OSNAMEtxt.setText(MetaOSName[1:len(MetaOSName)-1])
            if MetaOSVer[0] == '"':
                self.OSVERtxt.setText(MetaOSVer[1:len(MetaOSVer)-1])

            self.Bmenuwid.setEnabled(True)
            self.rightFrame.setVisible(False)
            self.Installingframe.setVisible(True)
            self.isExtracting = False

        else:
            # Installing Code
            print("Installing")
            for i in range(101):
                self.installprog.setValue(i)
                sleep(0.05)


    def openFileNameDialog( self ):
        options = QFileDialog.Options( )
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "Android Image Files (*.iso)", options=options)
        if fileName:
            self.Installbtn.setEnabled(True)
            self.Isonamevar = fileName
            if len(fileName) > 40:
                self.selectediso.setText('Iso : '+fileName[0:40]+'...')
            else:
                self.selectediso.setText('Iso : %s' % (fileName))

        else:
            self.Installbtn.setEnabled(False)
            self.selectediso.setText('Iso : None')
            self.Isonamevar = 'None'

    def OpenAbout( self ):
        self.abtwin = AboutWindow( )
        self.abtwin.setParent(self, Qt.Window)
        self.abtwin.show( )

    def OpenHelp( self ):
        self.hlpwin = HelpWindow( )
        self.hlpwin.setParent(self, Qt.Window)
        self.hlpwin.show( )

    def func_quit_all_windows( self ):
        sys.exit( )

        ############################################################


def main():
    app = QApplication(sys.argv)
    ex = Example( )
    sys.exit(app.exec_( ))


if __name__ == '__main__':
    main( )
