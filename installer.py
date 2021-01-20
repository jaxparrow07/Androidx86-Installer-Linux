#!/usr/bin/env python3

import sys
from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QApplication
from PyQt5.QtGui import QIcon

theme = open('app/MacOS.qss','r')


class Example(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        # Adding Side Options in Menu

        exitAct = QAction(QIcon('exit.png'), '&Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(qApp.quit)
        self.statusBar()

        selectiso = QAction(QIcon('exit.png'), '&Select iso', self)
        selectiso.setShortcut('Ctrl+F')
        selectiso.setStatusTip('Select iso file')
        selectiso.triggered.connect(qApp.quit)
        self.statusBar()

        AboutAct = QAction(QIcon('exit.png'), '&About', self)
        AboutAct.setShortcut('Ctrl+A')
        AboutAct.setStatusTip('About application')
        AboutAct.triggered.connect(qApp.quit)
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

        self.setStyleSheet(theme.read())
        self.setGeometry(550, 100, 370, 540)
        self.setWindowTitle('Simple menu')
        self.show()


def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
