# Nautilus-properties-previous-versions
This is a extension to Nautilus with Nautilus-Python to work with .snapshot folders in a network share.

## Description of the problem
When we have a mounted share with enabled snapshots in Microsoft Windows we can access to this information with the properties dialog, at the tab 'Previous Versions'

In GNU\Linux we can access via .snapshot folder but it's not user-friendly, I want to make an extension to nautilus in order to make these easier to the user.

## Solution
Make a python extension to access in a graphical way to the .snapshots folders.

### Tested in
* Ubuntu 14.04
* [Lliurex 15.05](http://www.lliurex.net)


## Install
It needs a dependency with the package *python-nautilus* and let the file *previous-versions-property-page.py* in */usr/share/nautilus-python/extensions/*

## TO-DO
* Translate the messages
* Make a copy button to copy folder/file with a dialog and a progressbar
* Make a restore button to restore folder/file to the original folder/file with a progressbar


## Links of info to make the script:
 * http://python-gtk-3-tutorial.readthedocs.io
