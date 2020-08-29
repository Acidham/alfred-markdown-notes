#!/usr/bin/python3
# -*- coding: utf-8 -*-

import datetime
import os
import re
import sys
from html.parser import HTMLParser
from urllib.request import unquote, urlopen

from Alfred3 import Tools
from MyNotes import Search


class Markdown(object):

    PANDOC = '/usr/local/bin/pandoc -f html -t markdown_mmd --strip-comments --atx-headers'

    def __init__(self, url):
        self.url = url
        self.html = self._fetchHtml()
        self.md = self._fetchMd()
        self.mdPageUrl = f"[{url}]({url})"

    def _fetchHtml(self):
        try:
            r = urlopen(self.url)
            response = r.read().decode('utf-8')
        except:
            response = f"<html><body><a href=\"{self.url}\">{self.url}</a></body></html>"
            pass
        return response

    def getMdUrl(self):
        return self.mdPageUrl

    def _fetchMd(self):
        try:
            cmd = f'{self.PANDOC} {self.url}'
            md = os.popen(cmd)
            resp = md.read()
        except:
            resp = f"[{self.url}]({self.url})"
            pass
        return resp

    def getMd(self):
        return self.md

    def getHtml(self):
        return self.html

    def getTitle(self):
        res = re.findall(
            r'<title>[\n\t\s]*(.+)[\n\t\s]*</title>', self.html, re.MULTILINE)
        return ''.join(res)

    def _markdownHeader(self):
        today = self.getTodayDate(fmt="%d.%m.%Y")
        return f"""---\nCreated: {today}\nTags: #WebClip\n---\n"""

    def getMarkdownContent(self):
        out = self._markdownHeader()
        out += self.getMd()
        out += u'\n---\n'
        out += self.getMdUrl()
        return out

    @staticmethod
    def getTodayDate(fmt="%d.%m.%Y"):
        now = datetime.datetime.now()
        return now.strftime(fmt)


def parseFilename(f):
    to_replace = ['/', '\\', ':', '|']
    tmp = f.strip()
    for i in to_replace:
        tmp = tmp.replace(i, '-')
    return tmp


def writeMarkdown(md_content, md_path):
    with open(md_path, "w+") as f:
        f.write(md_content)


mn = Search()
ext = mn.getNotesExtension()
p = mn.getNotesPath()
argv = Tools.getArgv(1)
url = argv if argv.startswith(
    'http://') or argv.startswith('https://') else str()

# TODO: When HTML is not fetchable, the URL will be used.
# Fix formatting from <url> to markdown url [title](url)

if url:
    Tools.notify('Fetch URL...', 'The Note will be opened after the import...')
    markdown = Markdown(url)
    today = markdown.getTodayDate(fmt="%d.%m.%Y")
    today_time = markdown.getTodayDate(fmt="%d-%m-%Y %H-%M")
    md = markdown.getMarkdownContent()
    file_name = parseFilename(markdown.getTitle())
    if file_name == str():
        file_name = Tools.strJoin('WebClip from ', today_time)

    fPath = os.path.join(p, f"{file_name}{ext}")
    writeMarkdown(md, fPath)
    sys.stdout.write(fPath)
