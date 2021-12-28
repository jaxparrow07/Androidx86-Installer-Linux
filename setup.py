import io
import os.path
from setuptools import setup

VERSION_PATH = os.path.join(
    os.path.dirname(__file__), 'app/VERSION.txt')
with io.open(VERSION_PATH, 'r', encoding='utf-8') as f:
  version = f.read().strip()

setup(
    name = "androidx86-installer",        # what you want to call the archive/egg
    version = version,
    packages=["app"],    # top-level python modules you can import like
                                #   'import foo'
    dependency_links = [],      # custom links to a specific project
    install_requires=[],
    extras_require={},      # optional features that other packages can require
                            #   like 'app[foo]'
    package_data = {"app": ["VERSION.txt"]},
    author="Jaxparrow",
    author_email = "jaxparrow07@pm.me",
    description = "A GUI android-x86 installer for the Linux platform",
    license = "GPL-2.0",
    keywords= "android-x86",
    url = "https://github.com/jaxparrow07/Androidx86-Installer-Linux",
    entry_points = {
        "console_scripts": [        # command-line executables to expose
            "app_in_python = app.main:main",
        ],
        "gui_scripts": []       # GUI executables (creates pyw on Windows)
    }
)
