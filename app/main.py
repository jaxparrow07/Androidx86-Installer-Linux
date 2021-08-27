"""Top-level implementation of the app program."""

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from subprocess import CalledProcessError, check_output
from random import randint
from webbrowser import open as web_open
import psutil
import configparser
import os
import sys


# 10 Important imports - Some are optimized to minimum imports

def fetchResource(res):
    pyroot = os.path.dirname(os.path.dirname(__file__))
    return pyroot + '/' + res


## Adx86-Installer - Important Variables ##

helptxt = """

Please read this if you don't know how to use

Installation Steps:-
    * Select a android image file
    
    * Choose Filesystem type
      ( Ext or OtherFS )
      -> Ext doesn't need data.img
      
    * Choose Data Size
      ( OtherFS Only )
      
    * Extracting Iso will take some time
      based on the filesize
      
    * OS Name and version
      ( Multiple GRUB Entries )
      -> This will automatically set them
         if they are specified.
         You need to set them manually if
         the don't.
         
Note : Currently only for Ubuntu and some debian based distros.
"""

#print("Starting app from " + pyroot)
version_name = open(fetchResource("app/VERSION.txt"), "r").read()
debug = True


def clickable(widget):
    class Filter(QObject):

        clicked = pyqtSignal()

        def eventFilter(self, obj, event):

            if obj == widget:
                if event.type() == QEvent.MouseButtonRelease:
                    if obj.rect().contains(event.pos()):
                        self.clicked.emit()
                        # The developer can opt for .emit(obj) to get the object within the slot.
                        return True

            return False

    filter = Filter(widget)
    widget.installEventFilter(filter)
    return filter.clicked


#====== Help Window to Shot helptxt ========#
class HelpWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.widget = QWidget(self)
        layout = QVBoxLayout(self)

        helptext = QLabel(helptxt)
        helptext.adjustSize()
        helptext.setFixedWidth(330)
        helptext.setWordWrap(True)
        helptext.setAlignment(Qt.AlignLeft)

        helpheading = QLabel("Installing")
        helpheading.adjustSize()
        helpheading.setFixedWidth(330)
        helpheading.setFont(QFont('Arial', 13))
        helpheading.setWordWrap(True)
        helpheading.setAlignment(Qt.AlignCenter)

        layout.addWidget(helpheading)
        layout.addWidget(helptext)

        layoutscrl = QScrollArea(self)
        layoutscrl.setFixedWidth(330)
        layoutscrl.setFixedHeight(330)
        qframe = QFrame()
        qframe.setLayout(layout)
        layoutscrl.setWidget(qframe)
        layout.setAlignment(Qt.AlignTop)

        self.setWindowTitle('Help')
        self.setGeometry(570, 190, 330, 330)
        self.setFixedWidth(330)
        self.setFixedHeight(330)


#====== About Window of Application ========#
class AboutWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.widget = QWidget(self)
        layout = QVBoxLayout(self)
        layout.addWidget(self.widget)
        pixmap = QPixmap(fetchResource("img/sg_logo.png"))
        pixmap = pixmap.scaled(150, 150, Qt.KeepAspectRatio)
        Pixmap_label = QLabel(self)
        Pixmap_label.setPixmap(pixmap)
        Pixmap_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(Pixmap_label)

        version_app = QLabel(version_name)
        version_app.setAlignment(Qt.AlignCenter)
        version_app.adjustSize()

        layout.addWidget(version_app)

        SG_Name = QLabel('Made with time & passion by SupremeGamers')
        SG_Name.setFont(QFont('Arial', 11))

        def openwebsite():
            web_open('https://supreme-gamers.com')

        webbtn = QPushButton('Visit Website')
        webbtn.clicked.connect(openwebsite)

        layout.addWidget(SG_Name)
        layout.addWidget(webbtn)
        layout.addWidget(QLabel(' '))
        author_name = QLabel('Programmed by Jaxparrow')
        author_name.setFont(QFont('Arial', 9))
        author_name.adjustSize()
        author_name.setAlignment(Qt.AlignCenter)
        layout.addWidget(author_name)
        layout.setAlignment(Qt.AlignCenter)
        self.setWindowTitle('About')
        self.setGeometry(570, 190, 330, 330)
        self.setFixedWidth(330)
        self.setFixedHeight(330)


#====== Main Window ======#
class Example(QMainWindow):


    def __init__(self, parent=None, frame=QFrame.Box):
        super().__init__()
        self.initUI()
        self.setAcceptDrops(True)




    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        self.fileName = files[0]


        if '.iso' in self.fileName:
            self.Pixmap_label.setPixmap(self.iso_loaded)
            if self.fileName:
                self.Installbtn.setEnabled(True)
                self.Isonamevar = self.fileName

                if len(self.fileName) > 35:
                    self.selectediso.setText('Iso : %s... (%0.2f GB)' % (
                        self.fileName[0:35], os.path.getsize(self.fileName) / 1024 / 1024 / 1024))

                    self.DropFile.setText('Iso : %s... (%0.2f GB)' % (
                        self.fileName[0:35], os.path.getsize(self.fileName) / 1024 / 1024 / 1024))
                else:
                    self.selectediso.setText('Iso : %s' % (self.fileName))

            else:
                self.Installbtn.setEnabled(False)
                self.selectediso.setText('Iso : None')
                self.Isonamevar = 'None'

    def showdialog(self, txtmessage, additionalinfo, detailedtext):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText(txtmessage)
        msg.setInformativeText(additionalinfo)
        msg.setWindowTitle("Androidx86-Installer has Encountered an error")
        if detailedtext != "none":
            msg.setDetailedText("The details are as follows: \n"+detailedtext)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.buttonClicked.connect(self.revertback)
        msg.exec_()

    def install_done(self, get_name):
        msg = QMessageBox()
        msg.setText("Successfully Installed")
        msg.setInformativeText(get_name+' has been installed Successfully')
        msg.setWindowTitle("Androidx86-Installer has Encountered an error")

        msg.setStandardButtons(QMessageBox.Ok)
        msg.buttonClicked.connect(self.revertback)
        msg.exec_()

    def initUI(self):
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        # Adding Side Options in Menu

        exitAct = QAction(QIcon(fetchResource('img/exit.png')), '&Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(qApp.quit)
        self.statusBar()

        selectiso = QAction(
            QIcon(fetchResource('img/iso.png')), '&Select iso', self)
        selectiso.setShortcut('Ctrl+F')
        selectiso.setStatusTip('Select iso file')
        selectiso.triggered.connect(self.openFileNameDialog)
        self.statusBar()

        AboutAct = QAction(
            QIcon(fetchResource('img/about.png')), '&About', self)
        AboutAct.setShortcut('Ctrl+A')
        AboutAct.setStatusTip('About application')
        AboutAct.triggered.connect(self.OpenAbout)
        self.statusBar()

        HelpAct = QAction(QIcon(fetchResource('img/help.png')), '&Help', self)
        HelpAct.setShortcut('Ctrl+H')
        HelpAct.setStatusTip('Help for  application')
        HelpAct.triggered.connect(self.OpenHelp)
        self.statusBar()

        self.Isonamevar = 'None'
        self.isExtracting = True
        self.session_id = ""
        self.prevfile = ""
        self.isInstalled = False
        self.globname = ""

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
        mlayout.setAlignment(Qt.AlignCenter)

        self.Toplayout = QVBoxLayout()
        self.Toplayout.setAlignment(Qt.AlignCenter)

        # Init Top Layout

        self.drop_here = QPixmap(fetchResource("img/drop_here.png"))
        self.drop_here = self.drop_here.scaled(70, 70, Qt.KeepAspectRatio)

        self.iso_loaded = QPixmap(fetchResource("img/image_loaded.png"))
        self.iso_loaded = self.iso_loaded.scaled(70, 70, Qt.KeepAspectRatio)

        self.Pixmap_label = QLabel(self)
        self.Pixmap_label.setPixmap(self.drop_here)
        self.Pixmap_label.setAlignment(Qt.AlignCenter)

        clickable(self.Pixmap_label).connect(self.openFileNameDialog)

        self.DropFile = QLabel("Drop file here ( or Click the icon )")
        self.DropFile.setAlignment(Qt.AlignCenter)

        self.selectediso = QLabel('Iso : None')
        self.selectediso.setAlignment(Qt.AlignLeft)
        self.OSNAMEtxt = QLineEdit()
        self.OSVERtxt = QLineEdit()

        self.InstallationFS = QComboBox()
        self.InstallationFS.addItems(['Ext', 'OtherFS'])
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

        getpart = os.popen(
            "grep '/dev/sd' '/proc/mounts' | awk '{print $1;}'").read()
        cpart = os.popen(
            "df -Th /home/ | head -n 2 | tail -n 1 | awk '{print $1;}'").read()
        root = os.popen(
            "df -Th / | head -n 2 | tail -n 1 | awk '{print $1;}'").read()

        if root != cpart:
            self.c_home = True
            getpart = getpart.replace(cpart, '').replace(root, '')
        else:
            self.c_home = False
            getpart = getpart.replace(root, '')

        self.Installationpart.addItem('Current Home Directory')
        for item in getpart.split():
            self.Installationpart.addItem(item)

        self.singlefileprog = QProgressBar()
        self.singlefileprog.setValue(0)
        self.currentfilename = QLabel('Current File : None')
        self.currentfilename.setAlignment(Qt.AlignLeft)

        instspacelay = QVBoxLayout()
        instspacelay.setAlignment(Qt.AlignTop)

        self.instspace = QWidget()
        self.instspace.setLayout(instspacelay)
        self.instspace.setFixedHeight(160)

        self.Toplayout.addWidget(self.Pixmap_label)
        self.Toplayout.addWidget(self.DropFile)


        # Extra Options layout

        self.ExtraOptlayout = QVBoxLayout()
        self.ExtraOptlayout.setAlignment(Qt.AlignTop)
        self.ExtraOptlayout.addWidget(QLabel('Optional Configuration'))

        # Custom configurable widgets
        self.gen_unins_checkbox = QCheckBox("Generate Uninstallation Script")
        self.gen_unins_checkbox.setChecked(True)
        self.ExtraOptlayout.addWidget(self.gen_unins_checkbox)

        self.ExtraOptlayout.addWidget(QLabel('GRUB Entry Options'))

        self.create_grub_entry = QCheckBox("Create GRUB Entry")
        self.create_grub_entry.setChecked(True)
        self.create_grub_entry.stateChanged.connect(self.Togglegrubsettings)
        self.ExtraOptlayout.addWidget(self.create_grub_entry)

        self.grub_settings = QVBoxLayout()

        # Custom grub settings
        self.grubset_use_submenu = QCheckBox("Use Submenu")
        self.grubset_add_glock = QCheckBox("Gearlock Recovery Modes")
        self.grubset_useicon = QCheckBox("Use Icon in entries")


        self.grub_settings.addWidget(self.grubset_use_submenu)
        self.grub_settings.addWidget(self.grubset_add_glock)
        self.grub_settings.addWidget(self.grubset_useicon)

        self.grub_settings_wid = QWidget()
        self.grub_settings_wid.setLayout(self.grub_settings)

        self.ExtraOptlayout.addWidget(self.grub_settings_wid)


        self.ExtraOptframe = QFrame()
        self.ExtraOptframe.setLayout(self.ExtraOptlayout)
        self.ExtraOptframe.setFrameShadow(QFrame.Raised)
        self.ExtraOptframe.setFrameShape(QFrame.StyledPanel)
        self.ExtraOptframe.setVisible(False)
        self.ExtraOptframe.setFixedHeight(370)


        self.Installinglayout = QVBoxLayout()
        self.Installinglayout.setAlignment(Qt.AlignTop)
        self.Installinglayout.addWidget(QLabel('OS Name:'))
        self.Installinglayout.addWidget(self.OSNAMEtxt)
        self.Installinglayout.addWidget(QLabel('OS Version:'))
        self.Installinglayout.addWidget(self.OSVERtxt)

        self.Installinglayout.addWidget(QLabel('Filesystem Type:'))
        self.Installinglayout.addWidget(self.InstallationFS)
        self.Installinglayout.addWidget(self.Datasizetxt)
        self.Installinglayout.addWidget(self.Datasize)
        self.Installinglayout.addWidget(QLabel('Installation Partition:'))
        self.Installinglayout.addWidget(self.Installationpart)

        self.Installinglayout.addWidget(self.instspace)
        self.Installinglayout.addWidget(self.currentfilename)
        self.Installinglayout.addWidget(self.singlefileprog)

        self.Installingframe = QFrame()
        self.Installingframe.setLayout(self.Installinglayout)
        self.Installingframe.setFrameShadow(QFrame.Raised)
        self.Installingframe.setFrameShape(QFrame.StyledPanel)
        self.Installingframe.setVisible(False)
        self.Installingframe.setFixedHeight(370)

        Bottomlayout = QVBoxLayout()
        Bottomlayout.setAlignment(Qt.AlignCenter)
        Bottomlayout.addWidget(QPushButton('Bottom'))

        Bottommenu = QHBoxLayout()
        Bottommenu.setAlignment(Qt.AlignVCenter)

        self.installprog = QProgressBar()
        self.installprog.setValue(0)

        # Init Bottom Toolbar
        self.Installbtn = QPushButton('Next')
        self.closebtn = QPushButton('Close')
        self.closebtn.clicked.connect(self.func_quit_all_windows)
        self.Installbtn.setEnabled(False)
        self.Installbtn.clicked.connect(self.Extracting)
        self.OSVERtxt.textChanged.connect(self.input_fields_check)
        self.OSNAMEtxt.textChanged.connect(self.input_fields_check)

        Bottommenu.addWidget(QLabel('            '))
        Bottommenu.addWidget(self.Installbtn)
        Bottommenu.addWidget(self.closebtn)

        self.Bmenuwid = QWidget()
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
        mlayout.addWidget(self.ExtraOptframe)
        mlayout.addWidget(self.installprog)
        mlayout.addWidget(self.Bmenuwid)



        Mainwidget = QWidget()
        Mainwidget.setLayout(mlayout)
        self.setCentralWidget(Mainwidget)

        ################### Properties ############################

        self.setGeometry(550, 100, 370, 540)
        self.setFixedWidth(370)
        self.setFixedHeight(540)
        self.setWindowTitle('Androidx86 Installer')
        pixmap = QPixmap(fetchResource('img/sg_logo.png'))
        pixmap = pixmap.scaled(20, 20, Qt.KeepAspectRatio)
        icon = QIcon(pixmap)
        self.setWindowIcon(icon)
        self.show()

    def changemethod(self):
        if self.InstallationFS.itemText(self.InstallationFS.currentIndex()) == 'Ext':
            self.Datasize.setVisible(False)
            self.Datasizetxt.setVisible(False)
        else:
            self.Datasize.setVisible(True)
            self.Datasizetxt.setVisible(True)

    def revertback(self):
        self.prevfile = self.fileName
        self.prevsessionid = self.session_id
        self.session_id = ""
        self.rightFrame.setVisible(True)
        self.ExtraOptframe.setVisible(False)
        self.Installingframe.setVisible(False)
        self.Isonamevar = 'None'
        self.isExtracting = True
        self.installprog.setValue(0)
        self.currentfilename.setText('Current file : None')
        self.singlefileprog.setValue(0)
        self.setAcceptDrops(False)
        self.DropFile.setText("Drop file here ( or Click the icon )")
        self.Pixmap_label.setPixmap(self.drop_here)

    def input_fields_check(self):
        if not self.isExtracting:
            if self.OSNAMEtxt.text() == "":
                self.Installbtn.setEnabled(False)
            elif self.OSVERtxt.text() == "":
                self.Installbtn.setEnabled(False)
            else:
                self.Installbtn.setEnabled(True)

    def Datachange(self):
        self.Datasizetxt.setText('Data Image Size: %i GB' %
                                 (self.Datasize.value()))

    def Extracting(self):
        if self.isExtracting == True:

            self.setAcceptDrops(False)

            self.session_id = '/tmp/'+'ax86_mount'
            self.Bmenuwid.setEnabled(False)


            if os.path.isdir(self.session_id):
                try:
                    output = check_output(["pkexec", "umount", self.session_id])
                    returncode = 0
                except CalledProcessError as e:
                    output = e.output
                    returncode = e.returncode
                    return

            else:
                 os.mkdir(self.session_id)


            try:
                output = check_output(["pkexec", "mount", "--options","loop",self.Isonamevar,self.session_id])
                returncode = 0
            except CalledProcessError as e:
                output = e.output
                returncode = e.returncode

            if returncode != 0:
                print("[!] ax86-Installer : Process Folder Create Failed")
                self.showdialog(
                    'Cannot Create Folder', 'Folder Creation cancelled by user', 'none')
                return


            if os.path.isfile(self.session_id+'/windows/config.ini'):
                config = configparser.ConfigParser()
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
            else:
                self.Installbtn.setEnabled(False)

            self.Bmenuwid.setEnabled(True)
            self.rightFrame.setVisible(False)
            self.Installingframe.setVisible(True)
            self.isExtracting = False


        elif self.isInstalled:
            if not self.ExtraOptframe.isVisible():
                self.ExtraOptions()
            else:
                # Complete Installation
                self.Finish_Install()
                print("Installation Complete")

        elif debug:
            self.isInstalled = True
            print("Skipped File Copy")
            self.Extracting()

        else:
            files = ['initrd.img','kernel', 'install.img', 'system.sfs',]

            optional_files = ['gearlock','ramdisk.img']

            for opt_file in optional_files:
                if os.path.isfile(self.session_id+'/'+opt_file):
                    files.append(opt_file)

            to_increase = 100 / len(files)

            partition = self.Installationpart.itemText(
                self.Installationpart.currentIndex())

            OS_NAME = self.OSNAMEtxt.text() + '-' + self.OSVERtxt.text()
            OS_NAME.replace(' ', '_')
            self.globname = OS_NAME

            # os.system('app/bin/unmounter ' + partition)

            if partition == 'Current Home Directory':
                home = True
            else:
                home = False

            if not home:
                try:
                    check_output(
                        ["umount", partition])
                except:
                    print("[!] ax86-Installer : Process Unmount Failed")
                    self.showdialog(
                        'Cannot Unmount', 'Unmounting Failed to some reasons', 'none')
                    return

            # os.system('app/bin/mounter ' + partition)
            if not home:
                try:
                    mdir = "/mnt/tmpadvin"
                    os.makedirs(mdir, exist_ok=True)
                    check_output(
                        ["mount", "-o", "loop", partition, mdir])
                except:
                    print("[!] ax86-Installer : Process Mount Failed")
                    self.showdialog(
                        'Cannot Mount', 'Mounting cancelled by user', 'none')
                    return

            if not home:
                hdd = psutil.disk_usage('/mnt/tmpadvin/')
            else:
                hdd = psutil.disk_usage('/home/')
            filesize = os.path.getsize(self.fileName)
            if hdd.free < filesize:
                print("[!] ax86-Installer : Not Enough Space in " +
                      self.Installationpart.itemText(self.Installationpart.currentIndex))
                self.showdialog('Error when copying files', 'Not Enough Space on the specified partition', detailedtext="""
Space required for installation : %d MB
Space Available on %s : %d MB
            
Free up some space and retry again.""" % (filesize / 1024 / 1024, self.Installationpart.itemText(self.Installationpart.currentIndex), hdd.free / 1024 / 1024))
                return

            if not home:
                if not os.path.isdir('/mnt/tmpadvin/'+OS_NAME+'/'):
                    os.mkdir('/mnt/tmpadvin/'+OS_NAME)
                    DESTINATION = '/mnt/tmpadvin/' + OS_NAME + '/'
                else:
                    self.showdialog('Folder Already Exists', 'Folder Creation Failed', detailedtext="""
The installation folder %s in %s already exists.
Please rename the folder or use other name in the Os name and Version field""" % (OS_NAME, partition))
                    return

            else:
                DESTINATION = '/home/' + OS_NAME + '/'
                dirname = '/home/' + OS_NAME

                if not os.path.isdir(dirname):
                    try:
                        output = check_output(["pkexec", "mkdir", dirname])
                        returncode = 0
                    except CalledProcessError as e:
                        output = e.output
                        returncode = e.returncode

                    if returncode != 0:
                        print("[!] ax86-Installer : Process Folder Create Failed")
                        self.showdialog(
                            'Cannot Create Folder', 'Folder Creation cancelled by user', 'none')
                        return
                else:
                    self.showdialog('Folder Already Exists', 'Folder Creation Failed', detailedtext="""
The installation folder %s already exists.
Please rename the folder or use other name in the Os name and Version field""" % (dirname))
                    return

                try:
                    output = check_output(["pkexec", "chmod", "777", dirname])
                    returncode = 0
                except CalledProcessError as e:
                    output = e.output
                    returncode = e.returncode

                if returncode != 0:
                    print("[!] ax86-Installer : Process Chmod Failed")
                    self.showdialog('Cannot Own Folder',
                                    'Chmod cancelled by user', 'none')
                    return

            for file in files:
                fsize = int(os.path.getsize(self.session_id+'/'+file))
                new = DESTINATION + file
                self.singlefileprog.setValue(0)
                self.currentfilename.setText('Current file : %s' % (file))
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
                self.installprog.setValue(
                    self.installprog.value() + int(to_increase))
            if self.installprog.value() != 100:
                self.installprog.setValue(100)

            if self.InstallationFS.itemText(self.InstallationFS.currentIndex()) == 'Ext':
                if not home:
                    os.mkdir('/mnt/tmpadvin/' + OS_NAME + '/data')
                    os.system('touch /mnt/tmpadvin/' + OS_NAME + '/findme')

                else:
                    DESTINATION = '/home/' + OS_NAME
                    os.mkdir(DESTINATION + '/data')
                    os.system('touch '+DESTINATION+'/findme')
            else:
                if not home:
                    file = 'of=/mnt/tmpadvin/' + OS_NAME + '/data.img'
                    file_n = '/mnt/tmpadvin/' + OS_NAME + '/data.img'
                    os.system('touch /mnt/tmpadvin/' + OS_NAME + '/findme')
                    hdd = psutil.disk_usage('/mnt/tmpadvin/')

                else:
                    file = 'of=/home/' + OS_NAME + '/data.img'
                    file_n = '/home/' + OS_NAME + '/data.img'
                    DESTINATION = '/home/' + OS_NAME
                    os.system('touch '+DESTINATION+'/findme')
                    hdd = psutil.disk_usage('/home/')

                bs = "1048576"
                bytes_dat = int(self.Datasize.value()) * 1024 * 1024 * 1024
                count = int(self.Datasize.value()) * 1024

                print("[*] ax86-Installer : Creating Data.img")

                if hdd.free < bytes_dat:
                    print("[!] ax86-Installer : Process Data Create Failed")
                    self.showdialog('Cannot Create data.img', 'Insufficient Space', detailedtext="""
Space required for Data.img : %d GB
Space Available : %0.2f GB""" % (self.Datasize.value(), hdd.free / 1024 / 1024 / 1024))
                    return
                else:

                    msg = QMessageBox()
                    msg.setWindowTitle("Info")
                    msg.setText(
                        "Please Wait until it creates Data img... Ok to Proceed")
                    msg.setFixedWidth(250)
                    msg.setFixedHeight(100)
                    x = msg.exec_()  # this will show our messagebox

                    try:
                        output = check_output(
                            ["pkexec", "dd", "if=/dev/zero", file, 'bs='+bs, 'count=0', 'seek='+str(count)]
                            )
                        returncode = 0
                    except CalledProcessError as e:
                        output = e.output
                        returncode = e.returncode

                    if returncode != 0:
                        print("[!] ax86-Installer : Process Data Create Failed")
                        self.showdialog('Cannot Create data.img',
                                        'Data Image creation Failed', 'none')
                        return

                    print("[*] ax86-Installer : Creating Superblocks for Data")

                    try:
                        output = check_output(["pkexec", "mkfs.ext4", file_n])
                        returncode = 0
                    except CalledProcessError as e:
                        output = e.output
                        returncode = e.returncode

                    if returncode != 0:
                        print("[!] ax86-Installer : Process Data Create Failed")
                        self.showdialog(
                            'Cannot Create data.img', 'Data Image creation Failed on Verificcation', 'none')
                        return

            if not home:
                try:
                    output = check_output(
                        ["umount",mdir])  # Something seems wrong here?
                    returncode = 0
                except CalledProcessError as e:
                    output = e.output
                    returncode = e.returncode

                if returncode != 0:
                    print("[!] ax86-Installer : Process Unmount Failed")
                    self.showdialog(
                        'Cannot Unmount', 'Unmounting failed due to some reasons', 'none')
                    return

            #print("[*] ax86-Installer : Creating GRUB Entries")
            msg = QMessageBox()
            msg.setWindowTitle("Info")
            msg.setText(
                "You can close the installer now or head to next step")
            msg.setFixedWidth(250)
            msg.setFixedHeight(100)
            x = msg.exec_()  # this will show our messagebox

            #ins_id = str(randint(100000, 99999999))

    def Finish_Install(self):
        self.install_done(self.globname)

    def ExtraOptions(self):
        self.Installingframe.setVisible(False)
        self.ExtraOptframe.setVisible(True)


    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.fileName, _ = QFileDialog.getOpenFileName(self, "Select an Android image", "",
                                                       "Android Image Files (*.iso)", options=options)

        if self.fileName:
            self.Installbtn.setEnabled(True)
            self.Isonamevar = self.fileName
            if len(self.fileName) > 35:
                self.selectediso.setText('Iso : %s... (%0.2f GB)' % (
                    self.fileName[0:35], os.path.getsize(self.fileName) / 1024 / 1024 / 1024))
            else:
                self.selectediso.setText('Iso : %s' % (self.fileName))

        else:
            self.Installbtn.setEnabled(False)
            self.selectediso.setText('Iso : None')
            self.Isonamevar = 'None'

    def Togglegrubsettings(self):
        if self.create_grub_entry.isChecked():
            self.grub_settings_wid.setEnabled(True)
        else:
            self.grub_settings_wid.setEnabled(False)


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
