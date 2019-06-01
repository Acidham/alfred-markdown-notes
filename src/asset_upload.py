import os
import sys
import urllib
from shutil import copy2

import MyNotes

ASSETS_FOLDER = '_NoteAssets'


def getAssetsFolder():
    my_notes = MyNotes.Search()
    notes_path = my_notes.getNotesPath()
    assets_path = notes_path + ASSETS_FOLDER
    if not(os.path.exists(assets_path)):
        os.mkdir(assets_path)
    return assets_path


def copyFile(source, target):
    file_name = str()
    if os.path.isfile(source):
        copy2(source, target)
        file_name = os.path.basename(source)
    else:
        raise ValueError
    return ASSETS_FOLDER + "/" + file_name


source_file = sys.argv[1]

target_folder = getAssetsFolder()
asset_file = copyFile(source_file, target_folder)

file_url = urllib.pathname2url(asset_file)
md_link = "[%s](%s)" % (os.path.basename(asset_file), file_url)

sys.stdout.write(md_link)
