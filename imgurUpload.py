#!/usr/bin/env python3
# imgurUpload.py -- upload image to Imgur

import gi, pprint
gi.require_version('Gimp', '3.0')
from gi.repository import Gimp
gi.require_version('GimpUi', '3.0')
from gi.repository import GimpUi
from gi.repository import GObject
from gi.repository import GLib
from gi.repository import Gio

import sys, os, tempfile
import gettext
_ = gettext.gettext
def N_(message): return message

def uploadToImgur(path):
    import requests, base64
    client_id = "f5f72730a82ec65"
    img_data = base64.b64encode(open(path, 'rb').read())
    data = {
        'image': img_data,
        'type': 'base64',
        # TODO: get input from user for title and description
        # 'name': 'my-filename.png',
        # 'title': 'my-title',
        # 'description': 'my-good-description'
    }
    url = 'https://api.imgur.com/3/upload'
    headers = {'Authorization': 'Client-ID ' + client_id}
    res = requests.post(url, data=data, headers=headers).json()
    pprint.pprint(res)
    assert res['status'] == 200 or res['status'] == 201
    return res['data']['link']

def saveToPNG(procedure, run_mode, image, drawable, args, data):
    """The function that actually does the work"""
    layer = image.merge_visible_layers(Gimp.MergeType.CLIP_TO_IMAGE)
    file_name = next(tempfile._get_candidate_names()) + ".png"
    numDrawables, interlace, compression = 1, 0, 9
    print(type(image))
    print(type(drawable))
    Gimp.get_pdb().run_procedure('file-png-save', [
        GObject.Value(Gimp.RunMode, Gimp.RunMode.NONINTERACTIVE),
        GObject.Value(Gimp.Image, image),
        GObject.Value(GObject.TYPE_INT, numDrawables),
        GObject.Value(Gimp.ObjectArray, Gimp.ObjectArray.new(Gimp.Drawable, [layer], False)),
        GObject.Value(Gio.File, Gio.File.new_for_path(file_name)),
        GObject.Value(GObject.TYPE_BOOLEAN, interlace),
        GObject.Value(GObject.TYPE_INT, compression),
        GObject.Value(GObject.TYPE_BOOLEAN, True), #bkgd
        GObject.Value(GObject.TYPE_BOOLEAN, True), #gama
        GObject.Value(GObject.TYPE_BOOLEAN, False),#offs
        GObject.Value(GObject.TYPE_BOOLEAN, True), #phys
        GObject.Value(GObject.TYPE_BOOLEAN, True), #time
        GObject.Value(GObject.TYPE_BOOLEAN, True), #transparent
    ])
    print("path: " + file_name)
    if (os.path.exists(file_name)):        
        imgur_link = uploadToImgur(file_name)
        clean = os.remove(file_name)
        print(imgur_link)
        Gimp.message("Sucessfully uploaded!\n{}".format(imgur_link))
    else:
        print("Error removing ", file_name)

class ImgurUpload (Gimp.PlugIn):
    
    ## Parameters ##
    def do_query_procedures(self):
        self.set_translation_domain("gimp30-python",
            Gio.file_new_for_path(Gimp.locale_directory()))
        return [ "python-fu-saveToPNG" ]

    def do_create_procedure(self, name):
        procedure = Gimp.ImageProcedure.new(self, name,
                                       Gimp.PDBProcType.PLUGIN,
                                       saveToPNG, None)
        procedure.set_image_types("*");
        procedure.set_icon_name(GimpUi.ICON_GEGL);
        procedure.set_documentation(N_("Upload image to Imgur"),
                                       "Upload image to Imgur",
                                       name);
        procedure.set_menu_label(N_("_Upload to Imgur"));
        procedure.set_attribution("Alex Bouchard",
                                  "(c) GPL V2.0 or later",
                                  "2020");
        procedure.add_menu_path('<Image>/File/');

        return procedure

Gimp.main(ImgurUpload.__gtype__, sys.argv)
