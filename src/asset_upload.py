#!/usr/bin/python3

import os
import sys
from shutil import copy2
from urllib.request import pathname2url

from MyNotes import Search

ASSETS_FOLDER = '_NoteAssets'


def getAssetsFolder():
    """
    Get Assets Upload Folder from config

    Returns:

        str: Asset Folder for md Notes
    """
    my_notes = Search()
    notes_path = my_notes.getNotesPath()
    assets_path = os.path.join(notes_path, ASSETS_FOLDER)
    if not(os.path.exists(assets_path)):
        os.mkdir(assets_path)
    return assets_path


def copyFile(source, target):
    """
    Copy file to target folder

    Args:

        source (str): Source File path
        target (str): Target folder

    Raises:

        ValueError: if source file does not exists

    Returns:

        str: path to file after copied
    """
    file_name = str()
    if os.path.isfile(source):
        copy2(source, target, follow_symlinks=True)
        file_name = os.path.basename(source)
    else:
        raise ValueError
    return os.path.join(ASSETS_FOLDER, file_name)


source_file = sys.argv[1]  # File path to asset

target_folder = getAssetsFolder()
asset_file = copyFile(source_file, target_folder)

file_url = pathname2url(asset_file)
asset_file = os.path.basename(asset_file)
md_link = f"[{asset_file}]({file_url})"

sys.stdout.write(md_link)
