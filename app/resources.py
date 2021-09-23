"""Module to get big strings"""

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
linux /{name}/kernel quiet root=/dev/ram0 androidboot.selinux=permissive SRC=/{osname}/ noibrs noibpb nopti nospectre_v2 nospectre_v1 l1tf=off nospec_store_bypass_disable no_stf_barrier mds=off intel_pstate=disable mitigations=off # {pid} - ax86-installer
initrd /{name}/initrd.img # {pid} - ax86-installer
}} # {pid} - ax86-installer
"""

