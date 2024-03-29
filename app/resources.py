"""Module to get big strings"""

"""UI"""

help_basic = """
<center>
<h2>Basic</h2>
</center>
<hr>
<h3>Selecting files</h3>
You can select android images (iso) by either dragging and dropping them onto the desired place or selecting from <b><i>File > Select Iso</i></b>

<h3>OS Name and Version</h3>
Allows you to create multiple installtions of the same android image

<h3>Installation Types</h3>
This installer supports Ext ( data folder ) installation and Other filesystems ( data.img upto 32 GB )

<h3>Finding Partition Name</h3>
<ul>
<li>Open your desired partition on a file manager</li>
<li>Open terminal by <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>F4</kbd> or <b><i>Right click > Open Terminal here</i></b> ( or use the terminal below if available )</li>
<li>Then execute <b><kbd>df -Th .</kbd></b> on the terminal to see the partition name ( sda2 etc.,. )</li>
</ul>

<h3>Uninstallation Script</h3>
Uninstallation script allows you to uninstall the android installation files ( grub entry if added ) easily and safely.
"""

help_advanced = """
<center>
<h2>Advanced</h2>
</center>
<hr>
<h3>Grub Entry</h3>
Grub entry will be enabled if the system supports it and there's no installation of Grub Customizer ( grub-customizer ). Else, it'll only show the option to copy the Grub entry code.

<h3>Adding Grub Entry</h3>
If you know how to add Grub entries manually by grub.cfg or other workarounds, you can paste the code. Or you can simply use Grub Customizer to add the entry and save it.

"""

help_issues = """
<center>
<h2>Issues</h2>
</center>
<hr>
If you've found any issues within the installer or if you can't install a specific android image.<br> Please report by opening an issue :
<a href=\"https://github.com/jaxparrow07/Androidx86-Installer-Linux/issues\">https://github.com/jaxparrow07/Androidx86-Installer-Linux/issues</a>
"""

about_thanks_to =  """
<b>AXON</b><br>
<i>For helping in refactoring the project and fixing a lot of code.</i> <br>
<br>
<b>Team Bliss</b><br>
<i>For supporting the project by promoting it.</i><br>
<br>
<b>Manky201 and Xtr ( Xttt )</b><br>
<i>For giving suggestions and ideas in Mounting and Image creation.</i><br>
"""

about_libraries_used = """Python modules:

    • PyQt5
    • subprocess
    • configparser
    • psutil

Uses some linux binaries too
"""

about_s1 = """Androidx86 Installer for Linux

(c) 2021, SupremeGamers

"""

################################################################################

"""Functional"""

custom_basic = """#!/bin/sh
exec tail -n +3 $0

# This file provides an easy way to add custom menu entries.  Simply type the
# menu entries you want to add after this comment.  Be careful not to change
# the exec tail line above.insmod all_video
"""

custom_template = """

menuentry '{osname}' {{ # {pid} - ax86-installer
insmod all_video # {pid} - ax86-installer
search --set=root --file /{name}/findme # {pid} - ax86-installer
linux /{name}/kernel root=/dev/ram0 acpi_osi=Linux mitigations=off androidboot.hardware=android_x86_64 androidboot.selinux=permissive SRC=/{osname}/ # {pid} - ax86-installer
initrd /{name}/initrd.img # {pid} - ax86-installer
}} # {pid} - ax86-installer
"""

custom_entry = """insmod all_video
search --set=root --file /{name}/findme
linux /{name}/kernel root=/dev/ram0 acpi_osi=Linux mitigations=off androidboot.hardware=android_x86_64 androidboot.selinux=permissive SRC=/{osname}/
initrd /{name}/initrd.img"""

uninstallation_script = """
#!/usr/bin/bash

# Script Generated by Androidx86Installer
# It is recommended to delete this file if you have no idea where this ( uninstall.sh ) file came from
# Auto uninstall script

grubconfig="/etc/grub.d/40_custom"
script_path="$(realpath $0)"
script_path=$(dirname "$script_path")
if [[ -f "$script_path/findme" ]] || [[ -f "$script_path/initrd.img" ]]  || [[ -f "$script_path/ramdisk.img" ]] || [[ -f "$script_path/system.sfs" ]] || [[ -f "$script_path/system.img" ]];then
  if [[ `whoami` != 'root' ]];then
    echo 'Run as root to Uninstall'
  else
    echo 'Uninstalling : {osname} '
    if [[ -f "$grubconfig" ]];then
        read -p "Do you want to remove GRUB Entry ( if added ) [ y/N ] :" g_in
        if [[ $g_in == "y" ]] || [[ $g_in == "y" ]];then
            echo 'Removing GRUB Entry'
            grep -v '# {pid} - ax86-installer' "$grubconfig" > tmpfile && mv tmpfile "$grubconfig"
            update-grub
        fi
    fi
    echo 'Removing Files'
    if [[ -d "$script_path/data" ]];then
      chattr -R -i "$script_path/data"
    fi
    rm "$script_path" -r
    echo 'Successfully Uninstalled {osname}'
    exit 0
  fi
else
  echo "Executing this from a non-android directory is dangerous"
  echo "It is recommended to delete this file if you have no idea where this ( uninstall.sh ) file came from"
  exit 1
fi
"""