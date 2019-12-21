# -*- coding: utf-8 -*-
import datetime
import os
import re
import urllib
from collections import Counter, OrderedDict

from Alfred import Tools


class Search(object):

    def __init__(self):
        self.extension = self.__buildNotesExtension()
        self.path = self.__buildNotesPath()

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
    def strJoin(*args):
        return str().join(args)

    def getNotesPath(self):
        return self.path

    def getNotesExtension(self):
        return self.extension

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
            r'#{1}(\w+)\s?', re.I) if tag == '' else re.compile(r'#{1}(' + tag + '\w*)\s?', re.I | re.UNICODE)
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

    @staticmethod
    def getTodayDate(fmt="%d.%m.%Y"):
        now = datetime.datetime.now()
        return now.strftime(fmt)

    @staticmethod
    def getUrlScheme(f):
        """
        Gets the URL Scheme setup in Alfred Preferences

        Args:
            f(str): md file to add at the end of url scheme

        Returns:
            str: URL scheme
        """
        url_scheme = Tools.getEnv('url_scheme')
        return Tools.strJoin(url_scheme, urllib.pathname2url(f))
