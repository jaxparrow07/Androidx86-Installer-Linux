#!/usr/bin/env python3

import sys
# from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
# from PyQt5 import QtWidgets, uic
helptxt = """Select an iso to be installed.
It must contain a system.img for system to be installed.
Make sure the iso is not broken and downloaded correctly.

Install to a specific partition."""

version_name = 'v0.02 Alpha'

class HelpWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.widget = QWidget(self)
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)
        helptext = QLabel(helptxt)
        helptext.adjustSize()
        helptext.setFixedWidth(330)
        helptext.setWordWrap(True)
        helptext.setAlignment(Qt.AlignLeft)
        layout.addWidget(helptext)

        self.setWindowTitle('Help')
        self.setGeometry(570, 190, 330, 330)
        self.setFixedWidth(330)
        self.setFixedHeight(330)


class AboutWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.widget = QWidget(self)
        layout = QVBoxLayout(self)
        layout.addWidget(self.widget)
        pixmap = QPixmap('app/sg_logo.png')
        pixmap = pixmap.scaled(150,150,Qt.KeepAspectRatio)
        Pixmap_label = QLabel(self)
        Pixmap_label.setPixmap(pixmap)
        Pixmap_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(Pixmap_label)
        # layout.addWidget(pixmap.scaled(100,100,Qt.KeepAspectRatio))

        version_app = QLabel(version_name)
        version_app.setAlignment(Qt.AlignCenter)
        version_app.adjustSize()

        layout.addWidget(version_app)

        SG_Name = QLabel('Made by SupremeGamers')
        SG_Name.setFont(QFont('Arial', 13))

        layout.addWidget(SG_Name)
        layout.addWidget(QLabel(' '))
        author_name = QLabel('Programmed by Jaxparrow')
        author_name.setFont(QFont('Arial',9))
        author_name.adjustSize()
        author_name.setAlignment(Qt.AlignCenter)
        layout.addWidget(author_name)
        layout.setAlignment(Qt.AlignCenter)
        self.setWindowTitle('About')
        self.setGeometry(570, 190, 330, 330)
        self.setFixedWidth(330)
        self.setFixedHeight(330)

class Example(QMainWindow):

    def __init__(self, parent=None, frame=QFrame.Box):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setAttribute(Qt.WA_DeleteOnClose,True)
        # Adding Side Options in Menu

        exitAct = QAction(QIcon('exit.png'), '&Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(qApp.quit)
        self.statusBar()

        selectiso = QAction(QIcon('exit.png'), '&Select iso', self)
        selectiso.setShortcut('Ctrl+F')
        selectiso.setStatusTip('Select iso file')
        selectiso.triggered.connect(self.openFileNameDialog)
        self.statusBar()

        AboutAct = QAction(QIcon('exit.png'), '&About', self)
        AboutAct.setShortcut('Ctrl+A')
        AboutAct.setStatusTip('About application')
        AboutAct.triggered.connect(self.OpenAbout)
        self.statusBar()

        HelpAct = QAction(QIcon('exit.png'), '&Help', self)
        HelpAct.setShortcut('Ctrl+H')
        HelpAct.setStatusTip('Help for  application')
        HelpAct.triggered.connect(self.OpenHelp)
        self.statusBar()

        ##################   Menubar  #############################

        menubar = self.menuBar()

        # Adding Top Menus
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(selectiso)
        fileMenu.addAction(exitAct)

        helpMenu = menubar.addMenu('&Help')
        helpMenu.addAction(HelpAct)
        helpMenu.addAction(AboutAct)

        ###################   MainUI   #############################

        # Init Base Layout
        mlayout = QVBoxLayout()
        mlayout.setAlignment(Qt.AlignTop)

        Toplayout = QVBoxLayout()
        Toplayout.setAlignment(Qt.AlignTop)

        # Init Top Layout
        self.selectediso = QLabel('Iso : None')
        self.selectediso.setAlignment(Qt.AlignCenter)
        self.OSNAMEtxt = QLineEdit()
        self.OSVERtxt = QLineEdit()
        Toplayout.addWidget(self.selectediso)
        Toplayout.addWidget(QLabel('OS Name'))
        Toplayout.addWidget(self.OSNAMEtxt)
        Toplayout.addWidget(QLabel('OS Version'))
        Toplayout.addWidget(self.OSVERtxt)




        Bottomlayout = QVBoxLayout()
        Bottomlayout.setAlignment(Qt.AlignCenter)
        Bottomlayout.addWidget(QPushButton('Bottom'))

        Bottommenu = QHBoxLayout()
        Bottommenu.setAlignment(Qt.AlignVCenter)

        # Init Bottom Toolbar
        self.Installbtn = QPushButton('Install')
        self.Installbtn.setEnabled(False)

        Bottommenu.addWidget(QLabel('            '))
        Bottommenu.addWidget(self.Installbtn)

        Bmenuwid = QWidget()
        Bmenuwid.setLayout(Bottommenu)
        Bmenuwid.setFixedHeight(60)

        self.Toplaywid = QWidget()
        self.Toplaywid.setLayout(Toplayout)
        self.Toplaywid.setFixedHeight(370)
        self.Toplaywid.setStyleSheet("background-color:#353535")

        self.Statustext = QLabel('NOT READY')
        self.Statustext.setFont(QFont('Arial',15))
        self.Statustext.setAlignment(Qt.AlignCenter)

        # Adding created widgets
        mlayout.addWidget(self.Toplaywid)
        mlayout.addWidget(QLabel(' '))
        mlayout.addWidget(QLabel(' '))
        mlayout.addWidget(self.Statustext)
        mlayout.addWidget(Bmenuwid)

        Mainwidget = QWidget()
        Mainwidget.setLayout(mlayout)
        self.setCentralWidget(Mainwidget)

        ################### Properties ############################
        self.setGeometry(550, 100, 370, 540)
        self.setFixedWidth(370)
        self.setFixedHeight(540)
        self.setWindowTitle('Androidx86 Installer')
        self.show()

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "Android Image Files (*.iso)", options=options)
        if fileName:
            self.Installbtn.setEnabled(True)
            self.selectediso.setText('Iso : Selected')
            self.Statustext.setText('READY')
            self.Statustext.setStyleSheet('color:#00C7B6')
        else:
            self.Installbtn.setEnabled(False)
            self.selectediso.setText('Iso : None')
            self.Statustext.setText('NOT READY')
            self.Statustext.setStyleSheet('color:#FFFFFF')

    def OpenAbout(self):
        self.abtwin = AboutWindow()
        self.abtwin.setParent(self, Qt.Window)
        self.abtwin.show()

    def OpenHelp(self):
        self.hlpwin = HelpWindow()
        self.hlpwin.setParent(self, Qt.Window)
        self.hlpwin.show()

    def func_quit_all_windows(self):
        sys.exit()

        ############################################################

def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
