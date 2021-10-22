GIMP plug-in to export your image to Imgur (for GIMP v2.10, v2.99 or v3.0)

Installation
============

To install this plugin, copy ``imgurUpload.py`` to your GIMP plugins folder, in a sub-directory. This
folder can be found by going to Edit -> Preferences -> Folders -> Plug-Ins. Restart
GIMP and the plugin can be accessed under the File menu.

Note: If you are using GIMP 2.99 beta's Flatpak, you will be missing Python's ``requests`` module.  If you are using Arch linux, you can find the latest GIMP at https://mirrors.zju.edu.cn/archlinuxcn/x86_64/ along with required gegl, babl and libart-lgpl packages (if you want to avoid compiling it yourself until a stable release comes out).
