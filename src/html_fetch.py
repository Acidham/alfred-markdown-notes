#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
import html2text  # https://github.com/aaronsw/html2text
import urllib2
import MyNotes
from Alfred import Tools
import sys
import re
import HTMLParser


class Markdown(object):

    def __init__(self, url):
        self.url = url
        self.html = self.fetchHtml()
        self.md = self.fetchMd()
        self.mdPageUrl = u"[%s](%s)" % (url.decode('utf-8'), url.decode('utf-8'))

    def fetchHtml(self):
        try:
            response = urllib2.urlopen(self.url)
            response = response.read().decode('utf-8')
        except:
            response = "<html><body><a href=\"" + self.url + "\">" + self.url + "</a></body></html>"
            pass
        return response

    def getMdUrl(self):
        return self.mdPageUrl

    def fetchMd(self):
        return html2text.html2text(self.fetchHtml())

    def getMd(self):
        return self.md

    def getHtml(self):
        return self.html

    def getTitle(self):
        res = re.findall(r'<title>[\n\t\s]*(.+)[\n\t\s]*</title>', self.html, re.MULTILINE)
        return self.htmlDecode(''.join(res))

    @staticmethod
    def htmlDecode(string):
        string = urllib2.unquote(string)
        return HTMLParser.HTMLParser().unescape(string).encode('utf-8')

    def markdownHeader(self):
        today = self.getTodayDate(fmt="%d.%m.%Y")
        return "---\n" \
               "Created: {date}\n" \
               "Tags: #WebClip #URL\n" \
               "---\n".format(date=today)

    def getMarkdownContent(self):
        out = self.markdownHeader()
        out += self.getMd()
        out += "\n---\n"
        out += self.getMdUrl()
        return out

    @staticmethod
    def getTodayDate(fmt="%d.%m.%Y"):
            now = datetime.datetime.now()
            return now.strftime(fmt)


def parseFilename(f):
    to_replace = ['/', '\\', ':', '|']
    tmp = f.decode('utf-8').strip()
    for i in to_replace:
        tmp = tmp.replace(i, '-')
    return tmp.encode('utf-8')


def writeMarkdown(md_content, md_path):
    with open(md_path, "w+") as f:
        f.write(md_content.encode('utf-8'))


mn = MyNotes.Search()
ext = mn.getNotesExtension()
p = mn.getNotesPath()
argv = Tools.getArgv(1)
url = argv if argv.startswith('http://') or argv.startswith('https://') else str()

# TODO: When HTML is not fetchable, the URL will be used. 
# Fix formatting from <url> to markdown url [title](url)

if url:
    markdown = Markdown(url)
    today = markdown.getTodayDate(fmt="%d.%m.%Y")
    today_time = markdown.getTodayDate(fmt="%d-%m-%Y %H-%M")
    md = markdown.getMarkdownContent()
    file_name = parseFilename(markdown.getTitle())
    if file_name == str():
        file_name = Tools.strJoin('WebClip from ', today_time)
    fPath = mn.strJoin(p, file_name, ext)
    writeMarkdown(md, fPath)
    sys.stdout.write(fPath)
