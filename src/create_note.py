#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys

import MyNotes
from Alfred import Tools


class QuerySplitter(object):
    """
    Split Query into title and tags

    Args:
        object (str): Query string
    """

    def __init__(self, query):
        self.title = str()
        self.tag_list = list()
        self.tags = str()
        self._split(query)

    def _split(self, query):
        term_list = query.split(' ')
        title_list = list()
        self.tag_list = list()
        for t in term_list:
            if str(t).startswith('#'):
                self.tag_list.append(t)
            else:
                title_list.append(t)
        self.title = ' '.join(title_list)
        self.tags = ' '.join(self.tag_list)


def parseFilename(f):
    tmp = f.decode('utf-8').strip()
    # tmp = tmp.translate(None, '.')
    for k, v in CHAR_REPLACEMENT_MAP.items():
        tmp = tmp.replace(k, v)
    return tmp.encode('utf-8')


def fallback_content():
    """
    get Fallback content

    Returns:
        str: Content
    """
    return "---\n" \
        "Created: {date}\n" \
        "Tags: \n" \
        "---\n" \
        "# {title}\n" \
        "```\n" \
        "This is the fallback Template.\n" \
        "Create your own template, see help!\n" \
        "```"


def readTemplate(file_path, tags='', **kwargs):
    """
    Read template

    Args:
        file_path (str): Path to Template file

    Returns:
        str: Content
    """
    template_tag = Tools.getEnv('template_tag')
    if '#' not in template_tag or template_tag == str():
        template_tag = '#Template'
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            content = f.read()
    else:
        content = fallback_content()
    content = content.replace(template_tag, '')
    for k, v in kwargs.iteritems():
        content = content.replace('{' + k + '}', v)
    tag_line = 'Tags: {0}'.format(tags)
    if tags:
        content = content.replace('Tags: ', tag_line)
    return content


def getDefaultDate():
    """
    Read default date format from environment variable
    :return: default date format file name or default format
    """
    d = Tools.getEnv('default_date_format')
    return "%d.%m.%Y %H.%M" if d == str() else d


def getDefaultTemplate():
    """
    Read default template setting from environment variable
    :return: default template file name
    """
    template = Tools.getEnv('default_template')
    return 'template.md' if template == str() else template


def getTemplate():
    # Get template path from previous wf step
    template = Tools.getEnv('template_path')
    notes_path = md.getNotesPath()
    default_template = getDefaultTemplate()
    return Tools.strJoin(notes_path, default_template) if template == str() else template


def getTargetFilePath(file_name):
    file_path = Tools.strJoin(p, file_name, ext)
    if os.path.isfile(file_path):
        new_file_name = Tools.strJoin(
            file_name, ' ', MyNotes.Search.getTodayDate(getDefaultDate()))
        file_path = Tools.strJoin(p, new_file_name, ext)
    return file_path


# Replacement map for Filename when new file created
CHAR_REPLACEMENT_MAP = {
    '/': '-',
    '\\': '-',
    ':': '-',
    '|': '-',
    ',': ''
}

# create MD search object
md = MyNotes.Search()

# Load Environment Variables
ext = md.getNotesExtension()
p = md.getNotesPath()
query = Tools.getArgv(1)
if query.isspace():
    query = "My Note {today}".format(today=md.getTodayDate(getDefaultDate()))
qs = QuerySplitter(query)
md_default_template = getDefaultTemplate()
f_name = parseFilename(qs.title)
fPath = getTargetFilePath(f_name)
# try to get template from previous Workflow or default template
md_template = getTemplate()

if query:
    today = md.getTodayDate(getDefaultDate())
    with open(fPath, "w+") as f:
        file_content = readTemplate(md_template, tags=qs.tags, date=today, title=qs.title)
        f.write(file_content)
    sys.stdout.write(fPath)
