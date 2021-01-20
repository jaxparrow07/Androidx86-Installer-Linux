#!/usr/bin/env python3

import sys
# from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
# from PyQt5 import QtWidgets, uic

class AboutWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.widget = QWidget(self)
        layout = QVBoxLayout(self)
        layout.addWidget(self.widget)
        label = QLabel("Sub Window",self)
        self.setWindowTitle('About')
        self.setGeometry(570, 190, 330, 330)

class Example(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setAttribute(Qt.WA_DeleteOnClose,True)
        # Adding Side Options in Menu

        exitAct = QAction(QIcon('exit.png'), '&Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(self.func_quit_all_windows)
        self.statusBar()

        selectiso = QAction(QIcon('exit.png'), '&Select iso', self)
        selectiso.setShortcut('Ctrl+F')
        selectiso.setStatusTip('Select iso file')
        selectiso.triggered.connect(qApp.quit)
        self.statusBar()

        AboutAct = QAction(QIcon('exit.png'), '&About', self)
        AboutAct.setShortcut('Ctrl+A')
        AboutAct.setStatusTip('About application')
        AboutAct.triggered.connect(self.OpenAbout)
        self.statusBar()

        HelpAct = QAction(QIcon('exit.png'), '&Help', self)
        HelpAct.setShortcut('Ctrl+H')
        HelpAct.setStatusTip('Help for  application')
        HelpAct.triggered.connect(qApp.quit)
        self.statusBar()

        ############################################################

        menubar = self.menuBar()

        # Adding Top Menus
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(selectiso)
        fileMenu.addAction(exitAct)

        helpMenu = menubar.addMenu('&Help')
        helpMenu.addAction(HelpAct)
        helpMenu.addAction(AboutAct)

        ############################################################

        self.setGeometry(550, 100, 370, 540)
        self.setWindowTitle('Androidx86 Installer')
        self.show()

    def OpenAbout(self):
        self.abtwin = AboutWindow()
        self.abtwin.setParent(self, Qt.Window)
        self.abtwin.show()

    def func_quit_all_windows(self):
        sys.exit()

        ############################################################

def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
