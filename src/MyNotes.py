# -*- coding: utf-8 -*-
import datetime
import os
import re
import urllib
from collections import Counter, OrderedDict

from Alfred import Tools


class Notes(object):

    # Replacement map for Filename when new file created
    CHAR_REPLACEMENT_MAP = {
        '/': '-',
        '\\': '-',
        ':': '-',
        '|': '-',
        ',': ''
    }

    # Fallback Content when no Template is available
    FALLBACK_CONTENT = "---\n" \
        "Created: {date}\n" \
        "Tags: \n" \
        "---\n" \
        "# {title}\n" \
        "```\n" \
        "This is the fallback Template.\n" \
        "Create your own template, see help!\n" \
        "```"

    def __init__(self):
        self.extension = self.__buildNotesExtension()
        self.path = self.__buildNotesPath()
        self.default_template = os.getenv('default_template')
        self.template_tag = os.getenv('template_tag')
        self.url_scheme = os.getenv('url_scheme')
        self.default_date_format = os.getenv('default_date_format')

    @staticmethod
    def __buildNotesExtension():
        ext = os.getenv('ext')
        if ext is None:
            ext = '.md'
        return ext if '.' in ext else str().join(['.', ext])

    @staticmethod
    def __buildNotesPath():
        user_dir = os.path.expanduser('~')
        path = os.getenv('path_to_notes')
        if not(path.startswith('/')):
            path = '/' + path
        if not(path.startswith('/Users')):
            path = user_dir + path
        if not (path.endswith('/')):
            path += '/'
        return path

    @staticmethod
    def getTodayDate(fmt="%d.%m.%Y"):
        now = datetime.datetime.now()
        return now.strftime(fmt)

    def getDefaultDate(self):
        """
        Read default date format from environment variable
        :return: default date format file name or default format
        """
        return "%d.%m.%Y %H.%M" if self.default_date_format == str() else self.default_date_format

    def getNotesPath(self):
        return self.path

    def getNotesExtension(self):
        return self.extension

    @staticmethod
    def strJoin(*args):
        return str().join(args)


class Search(Notes):

    def __init__(self):
        super(Search, self).__init__()

    def __OR(self, search_terms, content):
        restring = '|'.join(search_terms)
        regexp = re.compile(r'(%s)+' % restring, re.I)
        return True if len(re.findall(regexp, content)) > 0 else False

    def __AND(self, search_terms, content):
        length = 1
        for i in search_terms:
            i = '.' if i == '' else i
            regexp = re.compile(r'%s+' % i, re.I)
            length *= len(re.findall(regexp, content))
        return True if length > 0 else False

    def searchInFiles(self, search_terms, search_type):
        file_list = self.getFilesListSorted()
        new_list = list()
        if file_list is not None:
            for f in file_list:
                content = self._getFileContent(f['path'])
                if content != str() and (search_type == 'and' and self.__AND(search_terms, content)) or (
                        search_type == 'or' and self.__OR(search_terms, content)):
                    new_list.append(f)
        return new_list

    def url_search(self, search_terms):
        notes = self.searchInFiles(search_terms, 'and')
        note_list = list()
        if notes:
            for f in notes:
                note_title = f['title']
                note_path = f['path']
                content = self._getFileContent(f['path'])
                matches = re.findall(r'\[(.*)\]\((https?.*)\)', content)
                link_list = list()
                # TODO: Implement url only match, links without markdown syntax
                # url_only_matches = re.findall(r'https?://', content)
                for m in matches:
                    url_title = m[0]
                    url = m[1]
                    link_list.append({'url_title': url_title, 'url': url})
                note_list.append({'title': note_title, 'path': note_path, 'links': link_list})
        return note_list

    def getNoteTitle(self, path):
        content = self._getFileContent(path)
        title = self._chop(os.path.basename(path), self.extension)
        obj = re.search(r'^#{1}\s{1}(.*)', content, re.MULTILINE)
        if obj is not None:
            title = obj.group(1) if len(re.findall(r'\{.*\}', obj.group(1))) == 0 else title
        return title

    @staticmethod
    def _chop(theString, ext):
        if theString.endswith(ext):
            return theString[:-len(ext)]
        return theString

    def getFileMeta(self, path, item):
        """
        Get file meta data of given file
        :param path: file path
        :param item: meta data name
        :return: item str()
        """
        os.stat_float_times(True)
        file_stats = os.stat(path)
        switch = {
            'ctime': file_stats.st_birthtime,
            'mtime': file_stats.st_mtime,
            'size': file_stats.st_size
        }
        return switch[item]

    def getFilesListSorted(self, reverse=True):
        """
        Get list of files in directory as dict
        :param reverse: bool
        :return: list(dict())
        """
        err = 0
        file_list = list()
        try:
            file_list = os.listdir(self.path)
            # TODO: Enhancement Implement subdir scanning
            """
            for root, dirs, files in os.walk(self.path, topdown=False):
                for name in files:
                    if name.endswith(".md"):
                        file_list.append(name)
            """
        except OSError as e:
            err = e.errno
            pass
        if err == 0:
            seq = list()
            for f in file_list:
                f_path = self.strJoin(self.path, f)
                not (f.startswith('.')) and f.endswith(self.extension) and seq.append({
                    'filename': f,
                    'path': f_path,
                    'title': self.getNoteTitle(f_path),
                    'ctime': self.getFileMeta(f_path, 'ctime'),
                    'mtime': self.getFileMeta(f_path, 'mtime'),
                    'size': self.getFileMeta(f_path, 'size')
                })
            sorted_file_list = sorted(seq, key=lambda k: k['mtime'], reverse=reverse)
            return sorted_file_list

    def tagSearch(self, tag, sort_by='tag', reverse=False):
        i = {'tag': 0, 'count': 1}
        matches = list()
        sorted_file_list = self.getFilesListSorted()
        regex = re.compile(
            r'#{1}(\w+)\s?', re.I) if tag == '' else re.compile(r'#{1}(' + tag + r'\w*)\s?', re.I | re.UNICODE)
        for f in sorted_file_list:
            content = self._getFileContent(f['path'])
            if content != str():
                match_obj = re.search(r'\bTags:.*', content, re.IGNORECASE | re.UNICODE)
                if match_obj:
                    r = match_obj.group(0)
                    results = re.findall(regex, r)
                    matches.extend(results)

        counted_matches = Counter([v.lower() for v in matches])
        # Sorted by match counter x[1] if sort by key (tag name) is required change to x[0]
        sorted_matches = OrderedDict(
            sorted(counted_matches.items(), key=lambda x: x[i[sort_by]], reverse=reverse))

        return sorted_matches

    def todoSearch(self, todo):
        matches = list()
        sorted_file_list = self.getFilesListSorted()
        regex = re.compile(r'[-|\*] {1}\[ \] {1}(.+)', re.I) if todo == '' else re.compile(
            r'[-|\*] {1}\[ \] {1}(.*' + todo + '.+)', re.I)
        for f in sorted_file_list:
            content = self._getFileContent(f['path'])
            if content != str():
                results = re.findall(regex, content)
                for i in results:
                    r_dict = {
                        'path': f['path'],
                        'todo': i,
                        'filename': f['filename'],
                        'title': f['title'],
                        'mtime': self.getFileMeta(f['path'], 'mtime'),
                        'ctime': self.getFileMeta(f['path'], 'ctime')
                    }
                    matches.append(r_dict)
        ret_list_dict = sorted(matches, key=lambda k: k['ctime'], reverse=False)
        return ret_list_dict

    def _getFileContent(self, file_path):
        if str(file_path).endswith(self.extension):
            with open(file_path, 'r') as c:
                content = c.read()
        else:
            content = str()
        return content

    def isNoteTagged(self, file_path, tag):
        match = False
        with open(file_path, 'r') as c:
            lines = c.readlines()[0:5]
        for l in lines:
            match_obj = re.search(r'Tags:.*' + tag, l, re.IGNORECASE)
            if match_obj:
                match = True
                break
        return match

    @staticmethod
    def get_search_config(q):
        """
        Returns search config tuple

        Args:
            q (string): Search Query e.g. Searchterm1&Searchtem2

        Returns:
            tuple: Search Terms and operator
        """
        if '&' in q:
            s_terms = q.split('&')
            s_type = 'and'
        elif '|' in q:
            s_terms = q.split('|')
            s_type = 'or'
        else:
            s_terms = [q]
            s_type = 'or'
        return s_terms, s_type

    def getUrlScheme(self, f):
        """
        Gets the URL Scheme setup in Alfred Preferences

        Args:
            f(str): md file to add at the end of url scheme

        Returns:
            str: URL scheme
        """
        return self.strJoin(self.url_scheme, urllib.pathname2url(f))


class NewNote(Notes):

    def __init__(self, note_title, template_path=str(), tags=str(), content=str()):
        super(NewNote, self).__init__()
        self.tags = tags
        self.content = content
        self.note_title = note_title
        self.note_path = self.getTargetFilePath(self.parseFilename(note_title))
        # TODO: use only name instead of full path
        self.template_path = self.getTemplate(template_path)

    def getTargetFilePath(self, file_name):
        """

        construct markdown file path


        Returns:
            str: markdown file path
        """
        file_path = Tools.strJoin(self.path, file_name, self.extension)
        if os.path.isfile(file_path):
            new_file_name = Tools.strJoin(
                file_name, ' ', self.getTodayDate('%d_%m_%Y %H_%M_%S'))
            file_path = Tools.strJoin(self.path, new_file_name, self.extension)
        return file_path

    def getDefaultTemplate(self):
        """
        Read default template setting from environment variable
        :return: default template file name
        """
        return 'template.md' if self.default_template == str() else self.default_template

    def getTemplate(self, template_path):
        """

        Get template path from previous wf step, reads env variable

        Returns:
            str: path to template.md
        """
        notes_path = self.path
        default_template = self.getDefaultTemplate()
        return Tools.strJoin(notes_path, default_template) if template_path == str() else template_path

    def readTemplate(self, **kwargs):
        """
        Read template mardkown file and fill placeholder defined in template
        with data provides as kwargs

        Args:
            file_path (str): Path to Template file

        Returns:
            str: Content
        """
        if '#' not in self.template_tag or self.template_tag == str():
            template_tag = '#Template'
        if os.path.exists(self.template_path):
            with open(self.template_path, "r") as f:
                content = f.read()
        else:
            content = self.FALLBACK_CONTENT
        content = content.replace(self.template_tag, '')
        for k, v in kwargs.iteritems():
            content = content.replace('{' + k + '}', v)
        tag_line = 'Tags: {0}'.format(self.tags)
        if self.tags:
            content = content.replace('Tags: ', tag_line)
        return content

    def parseFilename(self, f):
        """
        Replace special characters in filename of md file

        Returns:
            str: filename
        """
        tmp = f.decode('utf-8').strip()
        for k, v in self.CHAR_REPLACEMENT_MAP.items():
            tmp = tmp.replace(k, v)
        return tmp.encode('utf-8')

    def create_note(self):
        with open(self.note_path, "w+") as f:
            default_date = self.getDefaultDate()
            file_content = self.readTemplate(
                date=self.getTodayDate(default_date), title=self.note_title)
            file_content = file_content + '\n' + self.content if self.content else file_content
            f.write(file_content)
        return(self.note_path)
