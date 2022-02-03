import os
import app.resources as resources
from shutil import which as sh_which
from datetime import datetime

class Utils():
    def __init__(self, current_dir):
        super().__init__()
        self.cwd = current_dir
        self.custom_40 = "/etc/grub.d/40_custom"
        self.log_prefix = {"warning":"WARN","error":"ERR","task":"TASK","info":"INFO","ok":"DONE"}

        if not os.path.isdir(self.cwd + "/.tmp/"):
            os.mkdir(self.cwd + "/.tmp/")


    def isGrubEntrySafe(self):
        return sh_which("grub-customizer") is None and sh_which("update-grub") is not None

    def Log(self,log_type, log_mesage):
        now = datetime.now()
        print(now.strftime("%H:%M:%S") + ": ax86-Installer - " + self.log_prefix[log_type] + " - " + log_mesage)

    def isCustomExists(self):
        return os.path.isfile(self.custom_40)

    def GenerateUnins(self, name, isHome, pid):

        if isHome:
            path = "/home/" + name + "/uninstall.sh"
        else:
            path = "/tmp/tmp"

        return True

    def getGrubCode(self, entry_name, isHome):

        path = entry_name
        if isHome:
            path = "home/" + entry_name

        return resources.custom_entry.format(osname=entry_name, name=path)


    def GenGrubEntry(self, entry_name, isHome, process):

        custom_path = self.cwd + "/.tmp/" + process + '.cfg'
        path = entry_name

        if isHome:
            path = "home/" + entry_name

        grub_code = resources.custom_template.format(osname=entry_name, name=path, pid=process)

        if not self.isCustomExists():
            grub_code = resources.custom_basic + grub_code

        with open(custom_path, 'w') as gfile:
            gfile.write(grub_code)

        # Some stuntman method to append the grub_config
        config_creation = os.system("cat %s | pkexec tee -a %s > /dev/null 2>&1" % (custom_path, self.custom_40))

        if config_creation == 0:
            os.remove(custom_path)
            returncode = os.system("pkexec update-grub")

            if returncode == 0:
                return True
            else:
                return False
        else:
            return False

