#!/usr/bin/python
# -*- coding: utf-8 -*-
import binascii
import hashlib
import logging
import mimetypes
import os
import re
import sys
import urllib

import evernote.edam.type.ttypes as Types
import evernote.edam.userstore.constants as UserStoreConstants
import markdown2
from evernote.api.client import EvernoteClient
from evernote.edam.error.ttypes import (EDAMErrorCode, EDAMNotFoundException,
                                        EDAMSystemException, EDAMUserException)

import MyNotes
from Alfred import Tools as Tools


class EvernoteUpload(object):

    def __init__(self, dev_token):
        myNotes = MyNotes.Search()
        self._connect_to_evernote(dev_token)
        self.notes_path = myNotes.getNotesPath()
        self.ext = myNotes.getNotesExtension()
        self.guid = str()

    def _connect_to_evernote(self, dev_token):
        user = None
        try:
            self.client = EvernoteClient(token=dev_token, sandbox=False)
            self.user_store = self.client.get_user_store()
            user = self.user_store.getUser()
            self.user_id = user.id
            self.shared_id = user.shardId
        except EDAMUserException as e:
            err = e.errorCode
            print("Error attempting to authenticate to Evernote: %s - %s" % (
                EDAMErrorCode._VALUES_TO_NAMES[err], e.parameter))
            return False
        except EDAMSystemException as e:
            err = e.errorCode
            print("Error attempting to authenticate to Evernote: %s - %s" % (
                EDAMErrorCode._VALUES_TO_NAMES[err], e.message))
            sys.exit(-1)

        if user:
            self.console_log(
                "Authenticated to evernote as user %s" % user.username)
            return True
        else:
            return False

    def _get_notebooks(self):
        note_store = self.client.get_note_store()
        notebooks = note_store.listNotebooks()
        return {n.name: n for n in notebooks}

    def _create_notebook(self, notebook):
        note_store = self.client.get_note_store()
        return note_store.createNotebook(notebook)

    def _update_notebook(self, notebook):
        note_store = self.client.get_note_store()
        note_store.updateNotebook(notebook)
        return

    def _check_and_make_notebook(self, notebook_name, stack=None):
        notebooks = self._get_notebooks()
        if notebook_name in notebooks:
            # Existing notebook, so just update the stack if needed
            notebook = notebooks[notebook_name]
            if stack:
                notebook.stack = stack
                self._update_notebook(notebook)
            return notebook
        else:
            # Need to create a new notebook
            notebook = Types.Notebook()
            notebook.name = notebook_name
            if stack:
                notebook.stack = stack
            notebook = self._create_notebook(notebook)
            return notebook

    def _create_evernote_note(self, notebook, filename):
        # Create the new note
        note = Types.Note()
        # Chop extension from filename and use it as note title
        note.title = Tools.chop(os.path.basename(filename), self.ext)
        note.notebookGuid = notebook.guid
        note.content = '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">'
        note.content += '<en-note>'
        md_content = self._get_md_content(filename)
        # Get Tag List from YAML Fonter
        tag_list = self._get_tag_list(md_content)
        # Remove YAML Fronter tags
        md_content = self._remove_yaml_fronter(md_content)
        # Read image links from MD
        file_list_in_md = self._get_images_in_md(md_content)

        # TODO: move to method
        file_hash_dict = dict()
        res = list()
        for f in file_list_in_md:
            file_path = self.notes_path + self._url_decode(f)
            with open(file_path, 'rb') as the_file:
                image = the_file.read()
            md5 = hashlib.md5()
            md5.update(image)
            the_hash = md5.digest()

            data = Types.Data()
            data.size = len(image)
            data.bodyHash = the_hash
            data.body = image

            resource = Types.Resource()
            resource.mime = mimetypes.guess_type(file_path)[0]
            resource.data = data
            # Now, add the new Resource to the note's list of resources
            res.append(resource)
            hash_hex = binascii.hexlify(the_hash)
            file_hash_dict.update({f: hash_hex})

        # Replace MD Link with ENML Link
        note.resources = res
        # Add Tag list from YAML
        note.tagNames = tag_list
        for md_link, hash_hex in file_hash_dict.items():
            en_link = '<en-media type="image/png" hash="' + hash_hex + '"/>'
            md_content = self._exhange_image_links(
                md_content, md_link, en_link)

        enml = markdown2.markdown(md_content).encode('utf-8')
        note.content += self.remove_invalid_urls(enml)
        note.content += '</en-note>'
        return note

    def upload_to_notebook(self, filename, notebookname, stack=None):
        # Check if the evernote notebook exists
        self.console_log("Checking for notebook named %s" % notebookname)
        notebook = self._check_and_make_notebook(notebookname, stack)

        self.console_log("Uploading %s to %s" % (filename, notebookname))

        note = self._create_evernote_note(notebook, filename)

        # Store the note in evernote
        note_store = self.client.get_note_store()
        created_note = note_store.createNote(note)

        guid = created_note.guid
        return self.get_note_app_link(guid)

    def _get_md_content(self, file_path):
        content = str()
        with open(file_path, 'r') as f:
            content = f.read()
        return content.decode('utf-8')

    def _remove_yaml_fronter(self, c):
        return self._delete_all_tags(c)

    def _get_images_in_md(self, md_content):
        new_img_list = list()
        img_list = re.findall(r'!\[.*\]\((.*)\)', md_content)
        # TODO enhance to accept other files and not only images
        # img_list = re.findall(r'\[.*\]\((.*)\)', md_content)
        for img in img_list:
            if not(str(img).startswith('http')):
                new_img_list.append(img)
        return new_img_list
        # return [self.notes_path + item for item in img_list]

    def _exhange_image_links(self, md_content, md_link, en_link):
        return re.sub(r'!\[.*\]\(' + md_link + '\)', en_link, md_content)

    def _url_decode(self, url):
        return urllib.url2pathname(url.encode('utf8'))

    def _url_encode(self, url):
        return urllib.pathname2url(url.encode('utf8'))

    def _delete_all_tags(self, md_content):
        return re.sub(r'---.*---', '', md_content, flags=re.DOTALL)

    def get_note_app_link(self, guid):
        """
        Get Note link to display note in Evernote client
        :param note_guid: int
        :return: url evernote://...
        """
        url = str()
        if guid is not '':
            url = "evernote:///view/%s/%s/%s/%s/" % (
                self.user_id, self.shared_id, guid, guid)
        return url

    def get_en_url(self, guid):
        url = str()
        if guid is not '':
            url = 'https://www.evernote.com/shard/%s/nl/%s/%s' % (
                self.shared_id, self.user_id, guid)
        return url

    def _get_tag_list(self, s):
        tag_line = re.findall(r'\bTags\b.*', s)
        all_tags = list()
        for t in tag_line:
            all_tags = re.findall(r'(#{1}[a-zA-Z0-9]*)', t)
        return [item.replace('#', '') for item in all_tags]

    def remove_invalid_urls(self, enml):
        enml_list = enml.split('\n')
        new_content_list = list()
        for line in enml_list:
            if "<a href=\"" in line:
                if "http" in line:
                    new_content_list.append(line)
                else:
                    obj = re.search(r'<a href=.*>(.*)</a>', line)
                    link_title = obj.group(1)
                    new_content_list.append("[" + link_title + self.ext + "]")
            else:
                new_content_list.append(line)
        return '\n'.join(new_content_list)

    @staticmethod
    def console_log(msg):
        # Create a custom logger
        logger = logging.getLogger(__name__)
        # Create handlers
        c_handler = logging.StreamHandler()
        c_handler.setLevel(logging.WARN)
        # Create formatters and add it to handlers
        c_format = logging.Formatter('%(message)s')
        c_handler.setFormatter(c_format)
        # Add handlers to the logger
        logger.addHandler(c_handler)
        logger.warn(msg)


auth_token = Tools.getEnv('evernote_auth_token')
f_path = Tools.getArgv(1)
# f_path = '/Users/jjung/Documents/Notes/test evernote import.md'
if auth_token == str():
    Tools.notify('Evernote authentication error',
                 'Set Evernote AuthToken in worfklow configuration!')
    sys.exit("Error")
elif f_path != str():
    p = EvernoteUpload(auth_token)
    note_app_link = p.upload_to_notebook(f_path, 'Inbox')
    if note_app_link is not str():
        Tools.notify('Upload in progress',
                     'The Note will be opened once uploaded!')
        sys.stdout.write(note_app_link)
    else:
        Tools.notify("Something went wrong")
