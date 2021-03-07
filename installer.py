#!/usr/bin/env python3

import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import configparser
import os
from subprocess import CalledProcessError, check_output
from random import randint
import psutil

helptxt = """Select an iso to be installed.
It must contain a system.img for system to be installed.
Make sure the iso is not broken and downloaded correctly.

Install to a specific partition."""

version_name = 'v0.74.0 Beta'

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

class Extracting(QWidget):
    def __init__( self ):
        super().__init__()
        self.widget = QWidget(self)
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)
        helptext = QLabel("Extracting")
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
        pixmap = QPixmap('/usr/share/androidx86-installer/img/sg_logo.png')
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

    def showdialog(self, txtmessage,additionalinfo,detailedtext):
        msg = QMessageBox( )
        msg.setIcon(QMessageBox.Warning)
        msg.setText(txtmessage)
        msg.setInformativeText(additionalinfo)
        msg.setWindowTitle("Androidx86-Installer has Encountered an error")
        if detailedtext != "none":
            msg.setDetailedText("The details are as follows: \n"+detailedtext)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.buttonClicked.connect(sys.exit)
        msg.exec_()

    def initUI( self ):
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        # Adding Side Options in Menu

        exitAct = QAction(QIcon('/usr/share/androidx86-installer/img/exit.png'), '&Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(qApp.quit)
        self.statusBar( )

        selectiso = QAction(QIcon('/usr/share/androidx86-installer/img/iso.png'), '&Select iso', self)
        selectiso.setShortcut('Ctrl+F')
        selectiso.setStatusTip('Select iso file')
        selectiso.triggered.connect(self.openFileNameDialog)
        self.statusBar( )

        AboutAct = QAction(QIcon('/usr/share/androidx86-installer/img/about.png'), '&About', self)
        AboutAct.setShortcut('Ctrl+A')
        AboutAct.setStatusTip('About application')
        AboutAct.triggered.connect(self.OpenAbout)
        self.statusBar( )

        HelpAct = QAction(QIcon('/usr/share/androidx86-installer/img/help.png'), '&Help', self)
        HelpAct.setShortcut('Ctrl+H')
        HelpAct.setStatusTip('Help for  application')
        HelpAct.triggered.connect(self.OpenHelp)
        self.statusBar( )

        self.Isonamevar = 'None'
        self.isExtracting = True
        self.session_id = ""

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

        os.system("grep '/dev/sd' '/proc/mounts' | awk '{print $1;}' > partlist.txt")
        f = open('partlist.txt','r')
        self.Installationpart.addItem('Current Ext4 Partition')
        for item in f.read().split():
            self.Installationpart.addItem(item)
        os.system("rm partlist.txt")

        # End of sample code

        self.singlefileprog = QProgressBar()
        self.singlefileprog.setValue(0)
        self.currentfilename = QLabel('Current File : None')
        self.currentfilename.setAlignment(Qt.AlignLeft)

        instspacelay = QVBoxLayout()
        instspacelay.setAlignment(Qt.AlignTop)
        instspacelay.addWidget(QLabel('Boot Flags: (leave if you don\'t know)'))

        self.instspace = QWidget()
        self.instspace.setLayout(instspacelay)
        self.instspace.setFixedHeight(180)

        self.Installinglayout = QVBoxLayout()
        self.Installinglayout.setAlignment(Qt.AlignTop)
        self.Installinglayout.addWidget(QLabel('OS Name:'))
        self.Installinglayout.addWidget(self.OSNAMEtxt)
        self.Installinglayout.addWidget(QLabel('OS Version:'))
        self.Installinglayout.addWidget(self.OSVERtxt)
        self.Installinglayout.addWidget(self.instspace)
        self.Installinglayout.addWidget(self.currentfilename)
        self.Installinglayout.addWidget(self.singlefileprog)

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
        pixmap = QPixmap('/usr/share/androidx86-installer/img/sg_logo.png')
        pixmap = pixmap.scaled(20, 20, Qt.KeepAspectRatio)
        icon = QIcon(pixmap)
        self.setWindowIcon(icon)
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

            self.session_id = '/tmp/'+'ax86_'+str(randint(100000,99999999))
            self.Bmenuwid.setEnabled(False)

            os.system("7z x '%s' -o%s -aoa" % (self.Isonamevar,self.session_id))

            if os.path.isfile(self.session_id+'/windows/config.ini'):
                config = configparser.ConfigParser( )
                config.read(self.session_id + '/windows/config.ini')
                MetaOSName = config.get('META-DATA', 'NAME')
                MetaOSVer = config.get('META-DATA', 'VERSION')

                if MetaOSName[0] == '"':
                    self.OSNAMEtxt.setText(MetaOSName[1:len(MetaOSName)-1])
                else:
                    self.OSNAMEtxt.setText(MetaOSName)

                if MetaOSVer[0] == '"':
                    self.OSVERtxt.setText(MetaOSVer[1:len(MetaOSVer)-1])
                else:
                    self.OSVERtxt.setText(MetaOSVer)

            self.Bmenuwid.setEnabled(True)
            self.rightFrame.setVisible(False)
            self.Installingframe.setVisible(True)
            self.isExtracting = False


        else:
            # Installing Code

            files = ['initrd.img', 'ramdisk.img','kernel','install.img','system.sfs']

            if os.path.isfile(self.session_id+'/gearlock'):
                files.append('gearlock')

            to_increase = 100 / len(files)

            partition = self.Installationpart.itemText(self.Installationpart.currentIndex())

            OS_NAME = self.OSNAMEtxt.text() + '_' + self.OSVERtxt.text()
            OS_NAME.replace(' ','_')

            # os.system('app/bin/unmounter ' + partition)

            try:
                output = check_output(["pkexec","/usr/share/androidx86-installer/bin/unmounter", partition])
                returncode = 0
            except CalledProcessError as e:
                output = e.output
                returncode = e.returncode

            if returncode != 0:
                print("[!] ax86-Installer : Process Unmount Failed")
                self.showdialog('Cannot Unmount','Unmounting cancelled by user','none')


            # os.system('app/bin/mounter ' + partition)

            try:
                output = check_output(["pkexec","/usr/share/androidx86-installer/bin/mounter", partition])
                returncode = 0
            except CalledProcessError as e:
                output = e.output
                returncode = e.returncode

            if returncode != 0:
                print("[!] ax86-Installer : Process Mount Failed")
                self.showdialog('Cannot Mount','Mounting cancelled by user','none')

            hdd = psutil.disk_usage('/mnt/tmpadvin/')
            filesize = os.path.getsize(self.fileName)
            if hdd.free < filesize:
                print("[!] ax86-Installer : Not Enough Space in "+self.Installationpart.itemText(self.Installationpart.currentIndex))
                self.showdialog('Error when copying files','Not Enough Space on the specified partition',detailedtext="""
Space required for installation : %d MB
Space Available on %s : %d MB
            
Free up some space and retry again.""" % (filesize / 1024 / 1024,self.Installationpart.itemText(self.Installationpart.currentIndex), hdd.free / 1024 / 1024))



            os.mkdir('/mnt/tmpadvin/'+OS_NAME)

            DESTINATION = '/mnt/tmpadvin/' + OS_NAME + '/'

            for file in files:
                fsize = int(os.path.getsize(self.session_id+'/'+file))
                new = DESTINATION + file
                self.singlefileprog.setValue(0)
                self.currentfilename.setText('Current file : %s' %(file))
                self.singlefileprog.setMaximum(fsize)
                with open(self.session_id+'/'+file, 'rb') as f:
                    with open(new, 'ab') as n:
                        buffer = bytearray()
                        while True:
                            buf = f.read(8192)
                            n.write(buf)
                            if len(buf) == 0:
                                break
                            buffer += buf
                            self.singlefileprog.setValue(len(buffer))
                self.installprog.setValue(self.installprog.value() + int(to_increase))
            if self.installprog.value() != 100:
                self.installprog.setValue(100)

            if self.InstallationFS.itemText(self.InstallationFS.currentIndex( )) == 'Ext':
                os.mkdir('/mnt/tmpadvin/' + OS_NAME + '/data')
                os.system('touch /mnt/tmpadvin/' + OS_NAME + '/findme')

            # os.system('app/bin/unmounter')

            try:
                output = check_output(["pkexec","/usr/share/androidx86-installer/bin/unmounter"])
                returncode = 0
            except CalledProcessError as e:
                output = e.output
                returncode = e.returncode

            if returncode != 0:
                print("[!] ax86-Installer : Process Unmount Failed")
                self.showdialog('Cannot Unmount','Unmounting cancelled by user','none')

    def openFileNameDialog( self ):
        options = QFileDialog.Options( )
        self.fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "Android Image Files (*.iso)", options=options)
        if self.fileName:
            self.Installbtn.setEnabled(True)
            self.Isonamevar = self.fileName
            if len(self.fileName) > 35:
                self.selectediso.setText('Iso : %s... (%0.2f GB)' % (self.fileName[0:35], os.path.getsize(self.fileName) / 1024 / 1024 / 1024))
            else:
                self.selectediso.setText('Iso : %s' % (self.fileName))

        else:
            self.Installbtn.setEnabled(False)
            self.selectediso.setText('Iso : None')
            self.Isonamevar = 'None'

        filesize = os.path.getsize(self.fileName)
        cp_space = psutil.disk_usage('/')
        if cp_space.free < filesize:
            self.Installbtn.setEnabled(False)
            print("[!] ax86-Installer : Not Enough Space to extract file")
            self.showdialog('Cannot Extract', 'Not enough space on current partition to extract files',detailedtext="""
Required space for extracting file/filesize : %d MB
Available space in the current partition : %d MB

Free up some space on current partition and try again.""" %(filesize / 1024 / 1024, cp_space.free / 1024 / 1024))

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
