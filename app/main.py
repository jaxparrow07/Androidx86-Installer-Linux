"""Top-level implementation of the app program."""

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from subprocess import CalledProcessError, check_output
from random import randint
# from webbrowser import open as web_open
import psutil
import configparser
import os
import sys


# 10 Important imports - Some are optimized to minimum imports
def fetchResource(res):
    pyroot = os.path.dirname(os.path.dirname(__file__))
    return pyroot + '/' + res


## Adx86-Installer - Important Variables ##
thanks_to =  """
<b>AXON</b><br>
<i>For helping in refactoring the project and fixing a lot of code.</i> <br>
<br>
<b>Team Bliss</b><br>
<i>For supporting the project by promoting it.</i><br>
<br>
<b>Manky201 and Xtr ( Xttt )</b><br>
<i>For giving suggestions and ideas in Mounting and Image creation.</i><br>
"""

libraries_used = """Python modules:

    • PyQt5
    • subprocess
    • configparser
    • psutil

Uses some linux binaries too
"""

about_s1 = """Androidx86 Installer for Linux
        
(c) 2021, SupremeGamers

"""

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
debug = False

# Function to make Widgets clickable
def clickable(widget):
    class Filter(QObject):
        clicked = pyqtSignal()
        def eventFilter(self, obj, event):

            if obj == widget:
                if event.type() == QEvent.MouseButtonRelease:
                    if obj.rect().contains(event.pos()):
                        self.clicked.emit()
                        return True
            return False
    filter = Filter(widget)
    widget.installEventFilter(filter)
    return filter.clicked


class DataWorker(QObject):

    finished = pyqtSignal()
    on_create_fail = pyqtSignal()
    on_verify_fail = pyqtSignal()

    def __init__(self,file,file_n,bs,count):
        super().__init__()
        self.file = file
        self.file_n = file_n
        self.bs = bs
        self.count = count

    def run(self):
        try:
            output = check_output(
                ["pkexec", "dd", "if=/dev/zero", self.file, 'bs=' + self.bs, 'count=0', 'seek=' + self.count]
            )
            returncode = 0
        except CalledProcessError as e:
            output = e.output
            returncode = e.returncode

        if returncode != 0:
            self.on_create_fail.emit()
            return

        print("[*] ax86-Installer : Creating Superblocks for Data")

        try:
            output = check_output(["pkexec", "mkfs.ext4", self.file_n])
            returncode = 0
        except CalledProcessError as e:
            output = e.output
            returncode = e.returncode

        if returncode != 0:
            self.on_verify_fail.emit()
            return

        self.finished.emit()


class Worker(QObject):

    finished = pyqtSignal()
    update_stats = pyqtSignal(int, str)
    update_prog = pyqtSignal(int)
    update_finish = pyqtSignal()


    def __init__(self,files,sessionid,destination):
        super().__init__()
        self.files = files
        self.sessionid = sessionid
        self.destin = destination

    def run(self):
        for file in self.files:
            fsize = int(os.path.getsize(self.sessionid+'/'+file))
            new = self.destin + file
            self.update_stats.emit(fsize,file)
            with open(self.sessionid+'/'+file, 'rb') as f:
                with open(new, 'ab') as n:
                    buffer = bytearray()
                    while True:
                        buf = f.read(8192)
                        n.write(buf)
                        if len(buf) == 0:
                            break
                        buffer += buf
                        # self.singlefileprog.setValue()
                        self.update_prog.emit(len(buffer))
            self.update_finish.emit()
        self.finished.emit()


class Loader(QWidget):
    def __init__(self,text):
        super().__init__()
        self.setWindowFlag(Qt.WindowCloseButtonHint, False)
        self.widget = QWidget(self)
        layout = QVBoxLayout(self)

        helpheading = QLabel(text)
        pulse_prog = QProgressBar()
        pulse_prog.setRange(0,0)

        layout.addWidget(helpheading)
        layout.addWidget(pulse_prog)
        layout.setAlignment(Qt.AlignCenter)

        self.setLayout(layout)

        self.setWindowTitle('Please Wait')
        self.setGeometry(570, 190, 330, 330)
        self.setFixedWidth(330)
        self.setFixedHeight(120)

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
        pixmap = QPixmap(fetchResource("img/mini_logo.png"))
        pixmap = pixmap.scaled(60, 60, Qt.KeepAspectRatio)
        Pixmap_label = QLabel()
        Pixmap_label.setPixmap(pixmap)
        Pixmap_label.setAlignment(Qt.AlignCenter)

        self.scroll_tab3 = QScrollArea()
        self.scroll_tab3.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll_tab3.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_tab3.setFrameShape(QFrame.NoFrame)

        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = self.scroll_tab3
        self.tabs.resize(300, 130)



        self.tabs.addTab(self.tab1, "About")
        self.tabs.addTab(self.tab2, "Libraries")
        self.tabs.addTab(self.tab3, "Thanks To")

        self.tab1.layout = QVBoxLayout()
        self.tab2.layout = QVBoxLayout()


        self.main_about = QLabel(about_s1)

        self.site_link = QLabel("<a href=\"https://supreme-gamers.com\">https://supreme-gamers.com</a>")
        self.site_link.setOpenExternalLinks(True)

        self.license_link = QLabel("<a href=\"https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html\">License: GNU General Public License Version 2</a>")
        self.license_link.setOpenExternalLinks(True)

        # Section Init
        self.tab1.layout.setAlignment(Qt.AlignTop)
        self.tab1.layout.addWidget(self.main_about)
        self.tab1.layout.addWidget(self.site_link)
        self.tab1.layout.addWidget(self.license_link)
        self.tab1.setLayout(self.tab1.layout)

        self.tab2.layout.setAlignment(Qt.AlignTop)
        self.tab2.layout.addWidget(QLabel(libraries_used))
        self.tab2.setLayout(self.tab2.layout)

        self.thanks_lbl = QLabel(thanks_to)
        self.thanks_lbl.setFixedWidth(280)
        self.thanks_lbl.setWordWrap(True)

        #self.scrl_lt = QVBoxLayout()
        #self.scrl_lt.addWidget(self.thanks_lbl)

        self.scroll_tab3.setWidget(self.thanks_lbl)


        hbox = QHBoxLayout()
        hbox.addWidget(Pixmap_label)
        vbox = QVBoxLayout()

        heading = QLabel("Androidx86 Installer")
        heading.adjustSize()
        heading.setFixedWidth(330)
        heading.setFont(QFont('Arial', 13))
        heading.setWordWrap(True)

        vbox.addWidget(heading)
        vbox.addWidget(QLabel(version_name))

        hbox.addLayout(vbox)


        close_box = QHBoxLayout()

        self.close_btn = QPushButton("Close")
        self.close_btn.clicked.connect(self.close)

        close_box.addWidget(self.close_btn)
        close_box.setAlignment(Qt.AlignRight)

        layout.addLayout(hbox)
        layout.addWidget(self.tabs)
        layout.addLayout(close_box)

        self.setLayout(layout)
        self.setWindowTitle('About')
        self.setGeometry(570, 190, 330, 200)
        self.setFixedWidth(330)
        self.setFixedHeight(290)


#====== Main Window ======#
class Example(QMainWindow):

    def __init__(self, parent=None, frame=QFrame.Box):
        super().__init__()
        self.initUI()
        self.setAcceptDrops(True)
        self.loadwin = Loader("Adding Boot Entry")
        # self.loadwin.setParent(self, Qt.Window)
        # self.Show_loader()

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
        exitAct = QAction(QIcon(fetchResource('img/exit.png')), '&Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(qApp.quit)
        self.statusBar()

        selectiso = QAction(QIcon(fetchResource('img/iso.png')), '&Select iso', self)
        selectiso.setShortcut('Ctrl+F')
        selectiso.setStatusTip('Select iso file')
        selectiso.triggered.connect(self.openFileNameDialog)
        self.statusBar()

        AboutAct = QAction(QIcon(fetchResource('img/about.png')), '&About', self)
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
        self.globmdir = ""

        ##################   Menubar  #############################

        menubar = self.menuBar()

        # Adding Top Menus
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(selectiso)
        fileMenu.addAction(exitAct)

        helpMenu = menubar.addMenu('&Help')
        helpMenu.addAction(HelpAct)
        helpMenu.addAction(AboutAct)

        ##################   MainUI   #############################

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
        #self.grubset_use_submenu = QCheckBox("Use Submenu")
        #self.grubset_add_glock = QCheckBox("Gearlock Recovery Modes")
        #self.grubset_useicon = QCheckBox("Use Icon in entries")


        #self.grub_settings.addWidget(self.grubset_use_submenu)
        #self.grub_settings.addWidget(self.grubset_add_glock)
        #self.grub_settings.addWidget(self.grubset_useicon)

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
            self.instspace.setFixedHeight(120)
            self.Datasizetxt.setVisible(False)
        else:
            self.Datasize.setVisible(True)
            self.instspace.setFixedHeight(0)
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
        self.Installbtn.setEnabled(False)

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
                self.extra_opt()
                print("Installation Complete")

        elif debug:
            self.isInstalled = True
            print("Skipped File Copy")
            self.Extracting()

        else:
            self.Bmenuwid.setEnabled(False)

            files = ['initrd.img','kernel', 'install.img', 'system.sfs']

            ## Necessary files checking
            for nes_file in files:
                if not os.path.isfile(self.session_id+'/'+nes_file):
                    print("[!] ax86-Installer : Process Data Create Failed")
                    self.showdialog('Invalid Iso',
                                    'Important file missing', detailedtext="""
Missing file : %s""" % (nes_file))
                    return

            optional_files = ['gearlock','ramdisk.img']
            for opt_file in optional_files:
                if os.path.isfile(self.session_id+'/'+opt_file):
                    files.append(opt_file)

            self.to_increase = 100 / len(files)

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
                self.mount_point = os.popen("lsblk -o MOUNTPOINT -n " + partition).read()
                self.mount_point = self.mount_point[:-1] + '/'

            self.globhome = home


            # os.system('app/bin/mounter ' + partition)

            if not home:
                hdd = psutil.disk_usage(self.mount_point)
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
                if not os.path.isdir(self.mount_point+OS_NAME+'/'):
                    os.mkdir(self.mount_point+OS_NAME)
                    DESTINATION = self.mount_point + OS_NAME + '/'
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

            # Disabling the configuration to avoid errors / changes in installation caused by changes in fields
            self.toggle_config(False)
            self.thread = QThread()

            self.worker = Worker(files,self.session_id,DESTINATION)
            self.worker.moveToThread(self.thread)

            self.thread.started.connect(self.worker.run)

            self.worker.finished.connect(self.thread.quit)
            self.worker.finished.connect(self.worker.deleteLater)
            self.thread.finished.connect(self.thread.deleteLater)

            self.worker.finished.connect(self.thread_finish)
            self.worker.update_prog.connect(self.thread_progress)
            self.worker.update_finish.connect(self.thread_mainprog)
            self.worker.update_stats.connect(self.thread_update)
            self.thread.start()


    # Thread Callbacks
    def thread_progress(self,int):
        self.singlefileprog.setValue(int)

    def thread_update(self,fsize,file):
        self.singlefileprog.setValue(0)
        self.currentfilename.setText('Current file : %s' % (file))
        self.singlefileprog.setMaximum(fsize)

    def thread_mainprog(self):
        self.installprog.setValue(
            self.installprog.value() + int(self.to_increase))

    def thread_finish(self):
        if self.installprog.value() != 100:
            self.installprog.setValue(100)
        self.postInstall()

    def toggle_config(self,state):
        self.OSNAMEtxt.setEnabled(state)
        self.OSVERtxt.setEnabled(state)
        self.InstallationFS.setEnabled(state)
        self.Installationpart.setEnabled(state)
        self.Datasize.setEnabled(state)

    def postInstall(self):
        if self.InstallationFS.itemText(self.InstallationFS.currentIndex()) == 'Ext':
            self.data_create = False

            if not self.globhome:
                os.mkdir(self.mount_point + self.globname + '/data')
                # os.system('touch '+ self.mount_point + self.globname + '/findme')
                output = check_output(
                    ["touch",self.mount_point + self.globname + '/findme' ]
                )
            else:
                DESTINATION = '/home/' + self.globname
                os.mkdir(DESTINATION + '/data')
                # os.system('touch ' + DESTINATION + '/findme')
                output = check_output(
                    ["touch",DESTINATION+'/findme' ]
                )
        else:
            self.data_create = True
            if not self.globhome:
                file = 'of='+ self.mount_point + self.globname + '/data.img'
                file_n = self.mount_point + self.globname + '/data.img'

                output = check_output(
                    ["touch",self.mount_point + self.globname + '/findme' ]
                )

                hdd = psutil.disk_usage(self.mount_point)

            else:
                file = 'of=/home/' + self.globname + '/data.img'
                file_n = '/home/' + self.globname + '/data.img'
                DESTINATION = '/home/' + self.globname

                output = check_output(
                    ["touch",DESTINATION+'/findme']
                )

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

                self.datathread = QThread()

                self.dataworker = DataWorker(file,file_n,bs,str(count))
                self.dataworker.moveToThread(self.datathread)

                self.datathread.started.connect(self.dataworker.run)

                self.dataworker.finished.connect(self.datathread.quit)
                self.dataworker.finished.connect(self.dataworker.deleteLater)
                self.datathread.finished.connect(self.datathread.deleteLater)

                self.dataworker.finished.connect(self.data_create_finish)
                self.dataworker.on_create_fail.connect(self.data_create_fail)
                self.dataworker.on_verify_fail.connect(self.data_verify_fail)
                self.datathread.start()


        # Will continue installtion if data image is not created otherwise it will wait for callback
        if not self.data_create:
            msg = QMessageBox()
            msg.setWindowTitle("Info")
            msg.setText(
                "You can close the installer now or head to next step")
            msg.setFixedWidth(250)
            msg.setFixedHeight(100)
            x = msg.exec_()  # this will show our messagebox

            self.toggle_config(True)
            self.isInstalled = True
            self.Bmenuwid.setEnabled(True)


    def data_create_finish(self):
        # print("[*] ax86-Installer : Creating GRUB Entries")
        msg = QMessageBox()
        msg.setWindowTitle("Info")
        msg.setText(
            "You can close the installer now or head to next step")
        msg.setFixedWidth(250)
        msg.setFixedHeight(100)
        x = msg.exec_()  # this will show our messagebox

        self.toggle_config(True)
        self.isInstalled = True
        self.Bmenuwid.setEnabled(True)

    def data_create_fail(self):
        print("[!] ax86-Installer : Process Data Create Failed")
        self.showdialog('Cannot Create data.img',
                        'Data Image creation Failed', 'none')
        return

    def data_verify_fail(self):
        print("[!] ax86-Installer : Process Data Create Failed")
        self.showdialog(
            'Cannot Create data.img', 'Data Image creation Failed on Verification', 'none')
        return

    def extra_opt(self):

        # Write code to generate Grub entry and Uninstallation
        if (self.create_grub_entry.isChecked()):
            # Code to create grub entry
            print("Creating grub entry")

        if (self.gen_unins_checkbox.isChecked()):
            # Code to generate uninstallation script
            print("Generating Uninstallation Script")

        # Finish installation if none
        self.Finish_Install()

    def closeEvent(self, event):
        self.loadwin.close()
        event.accept()

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
            self.Pixmap_label.setPixmap(self.iso_loaded)
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

    def Togglegrubsettings(self):
        if self.create_grub_entry.isChecked():
            self.grub_settings_wid.setEnabled(True)
        else:
            self.grub_settings_wid.setEnabled(False)


    def Show_loader(self):
        self.loadwin.show()

    def OpenAbout(self):
        self.abtwin = AboutWindow()
        self.abtwin.setParent(self, Qt.Window)
        self.abtwin.show()

    def OpenHelp(self):
        self.hlpwin = HelpWindow()
        self.hlpwin.setParent(self, Qt.Window)
        self.hlpwin.show()

    def func_quit_all_windows(self):
        self.loadwin.close()
        sys.exit()

        ############################################################


def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
