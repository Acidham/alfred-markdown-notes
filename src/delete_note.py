#!/usr/bin/python

import os
import re
import shutil
import sys
import urllib

from Alfred import Tools as Tools
from MyNotes import Search


def rmDir(path, ignore_errors=True):
    """
    Remove directory and it's content

    Args:
        path (string): path to specific markdown notes
        ignore_errors (bool, optional): Ignore errors. Defaults to True.

    Returns:
        bool: True in case removal was successful otherwise False
    """
    if os.path.exists(path):
        shutil.rmtree(path, ignore_errors)
        return not (os.path.exists(path))
    else:
        return False


def rmFile(path):
    """

    Remove file of a given path if

    Returns:
        bool: True if successful other False
    """
    path = urllib.url2pathname(path)
    if os.path.isfile(path) and os.path.exists(path):
        os.remove(path)
        return not (os.path.exists(path))
    else:
        return False


def getFileQuery(q):
    return q.split('|') if '|' in q else [q, str()]


def getAssetsLinks(parent_path, p):
    def is_in_notes(f_path):
        return not (str(f_path).startswith('..')) and not (str(f_path).startswith('/'))
    with open(p, 'r') as f:
        content = f.read()
    matches = re.findall(r'\[.*\]\((.*)\)', content)
    return [os.path.join(parent_path, m) for m in matches if is_in_notes(m)]


mn = Search()

# Load extentions env variables from settings
ext = mn.getNotesExtension()
# Get all files which needs to be deleted from input
files_to_delete = sys.argv[1:]

return_text = str()
for query in files_to_delete:
    file_path, last_query = getFileQuery(query)
    if os.path.isfile(file_path) and file_path.endswith(ext):
        file_name = os.path.basename(file_path)
        # Search for links to other assets and delete each file
        parent = mn.getNotesPath()
        assetfile_links = getAssetsLinks(parent, file_path)
        is_assetfile_deleted = False
        for l in assetfile_links:
            # Avoid Markdown file removal
            if not(l.endswith(ext)):
                is_assetfile_deleted = rmFile(l)

        # Delete Assets Folder
        remove_ext = len(ext)
        assets_path = Tools.strJoin(file_path[:-remove_ext], ".assets")
        assets_path_legacy = Tools.strJoin(file_path[:-remove_ext])
        is_asset_deleted = rmDir(assets_path) or rmDir(assets_path_legacy) or is_assetfile_deleted

        # Finally delete the MD File
        is_file_deleted = rmFile(file_path)

        # Create Notification Message
        if len(files_to_delete) == 1:
            return_text = '- MD Note DELETED'if is_file_deleted else "Cannot delete file: {0}".format(
                file_name)
            return_text += '\n- Assets DELETED' if is_asset_deleted else str()

if len(files_to_delete) > 1:
    return_text = "{0} Notes and coresponding Assets deleted".format(len(
        files_to_delete))

Tools.notify('MD Note deleted!', return_text)

sys.stdout.write(last_query)
