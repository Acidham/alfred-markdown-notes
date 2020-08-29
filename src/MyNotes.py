#!/usr/bin/python3
# -*- coding: utf-8 -*-

import datetime
import os
import re
import sys
from collections import Counter, OrderedDict
from unicodedata import normalize
from urllib.request import pathname2url

from Alfred3 import Tools


class Notes(object):

    REPL_MAP = {
        '[': '',
        ']': ' ',
        '(': '',
        ')': ' ',
        '\n': ' ',
        '*': ' ',
        ',': ' ',
        '.': ' ',
        '-': ' ',
        ':': ' ',
        '?': ' ',
        '!': ' '
    }

    # Replacement map for Filename when new file created
    CHAR_REPLACEMENT_MAP = {
        '/': '-',
        '\\': '-',
        ':': '-',
        '|': '-',
        ',': '',
        '#': '-'
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
        if not(self.isPython3()):
            Tools.log("PYTHON VERSION:", sys.version)
            raise ModuleNotFoundError("Python version 3.7.0 or higher required!")
        self.extension = self.__buildNotesExtension()
        self.path = self.__buildNotesPath()
        self.default_template = os.getenv('default_template')
        self.template_tag = os.getenv('template_tag')
        self.url_scheme = os.getenv('url_scheme')
        self.search_yaml_tags_only = Tools.getEnvBool('search_yaml_tags_only')
        self.default_date_format = os.getenv('default_date_format')
        self.exact_match = Tools.getEnvBool('exact_match')
        self.todo_newest_oldest = Tools.getEnvBool('todo_newest_oldest')

    @staticmethod
    def isPython3() -> bool:
        """
        Check if script is executed with Python 3.7 or higher

        Returns:

            bool: True if Python3 else false
        """
        is_python3 = True
        if sys.version_info < (3, 7):
            is_python3 = False
        return is_python3

    @staticmethod
    def __buildNotesExtension() -> str:
        """
        Get notes extension configured in workflow preference

        Returns:

            str: extension incl. dot e.g. .md

        """
        ext = os.getenv('ext')
        if ext is None:
            ext = '.md'
        return ext if '.' in ext else str().join(['.', ext])

    @staticmethod
    def __buildNotesPath() -> str:
        """
        Create Notes path configured in preferences

        Returns:

            str: home path to notes directory

        """
        user_dir = os.path.expanduser('~')
        path = os.getenv('path_to_notes')
        if path.startswith('~'):
            path = path.replace('~', user_dir)
        if not(path.startswith('/')):
            path = os.path.join("/", path)
        if not(path.startswith('/Users')):
            path = os.path.join(user_dir, path)
        if not(os.path.exists(path)):
            sys.stderr.write(f"ERROR: {path} is not a valid notes directory. Add a valid path for path_to_notes")
            sys.exit(0)
        return path

    @staticmethod
    def getTodayDate(fmt: str = "%d.%m.%Y") -> str:
        """
        Get today's date

        Args:

            fmt (str, optional): Date format. Defaults to "%d.%m.%Y".

        Returns:

            str: formatted today's date

        """
        now = datetime.datetime.now()
        return now.strftime(fmt)

    def getDefaultDate(self) -> str:
        """
        Read default date format from environment variable

        Returns:

            str: default date format file name or default format
        """
        return "%d.%m.%Y %H.%M" if self.default_date_format == str() else self.default_date_format

    def getNotesPath(self) -> str:
        """
        Get path to notes home directory

        Returns:

            str: Path to notes home

        """
        return self.path

    def getNotesExtension(self) -> str:
        """
        Get notes extension from .env

        Returns:

            str: File extension for md files

        """
        return self.extension

    @staticmethod
    def strJoin(*args: str) -> str:
        """
        Join multiple strings

        Arguments:

            *args (str): strings to join

        Returns:

            (str): joined string

        """
        return str().join(args)

    @staticmethod
    def strReplace(text: str, replace_map: dict, lowercase: bool = True) -> str:
        """
        Replace in text from a replacement map

        Args:

            text (str): The string which needs to be processed
            replace_map (dict): dict with search:replace

        Returns:

            str : String with replacements

        """
        for k in replace_map.keys():
            text = text.replace(k, replace_map[k])
        return text.lower() if lowercase else text


class Search(Notes):
    """
    Search in Notes

    Returns:

        (object): a Search object

    """

    def __init__(self):
        super(Search, self).__init__()

    def _match(self, search_terms, content, operator):
        """
        Find matches of search_terms list with OR or AND

        Args:

            search_terms (list): Search terms
            content (str): Text to search
            operator (str): 'OR' or 'AND'

        Returns:

            bool: True if search terms matches

        """
        content = content.lower()
        content = self.strReplace(content, self.REPL_MAP)
        word_list = content.split(' ')
        word_list = [self._chop(w, '#') for w in word_list]
        search_terms = [s.lower() for s in search_terms]
        match = False
        matches = list()

        for st in search_terms:
            search_str = st.replace('*', str())
            # search if search term contains a whitespace
            if ' ' in st:
                regexp = re.compile(f'({st})', re.I)
                match = True if len(re.findall(regexp, content)) > 0 else False
            # search if wildcard search in the end
            elif st.endswith('*'):
                match_list = [x for x in word_list if x.startswith(search_str)]
                match = True if len(match_list) > 0 else False
            # search if wildcard search in front
            elif st.startswith('*'):
                match_list = [x for x in word_list if x.endswith(search_str)]
                match = True if len(match_list) > 0 else False
            # search if exact match is true
            elif self.exact_match:
                match = True if search_str in word_list else False
            # search with exact match is false
            else:
                match = True if search_str in str(word_list) else False
            matches.append(match)
        match = all(matches) if operator == 'AND' else any(matches)
        return match

    def notes_search(self, search_terms: list, search_type: str) -> list:
        """
        Search with search terms in all markdown files

        Args:

            search_terms (list): Search terms in a list
            search_type (str): OR or AND search

        Returns:

            list: list of files matches the search

        """
        file_list = self.getFilesListSorted()
        #search_terms = [normalize('NFD', s.decode('utf-8')) for s in search_terms]
        new_list = list()
        if file_list is not None:
            for f in file_list:
                content = self._getFileContent(f['path'])
                if content != str() and (search_type == 'and' and self._match(search_terms, content, 'AND')) or (
                        search_type == 'or' and self._match(search_terms, content, 'OR')):
                    new_list.append(f)
        return new_list

    def url_search(self, search_terms: list) -> list:
        """
        Search Notes with bookmarks (URLs)

        Args:

            search_terms (list): Search terms in a list

        Returns:

            list: List of Notes found

        """
        notes = self.notes_search(search_terms, 'and')
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

    def getNoteTitle(self, path: str) -> str:
        """
        Get the title of a note

        Args:

            path (str): Full path to note

        Returns:

            str: Title of the note
        """
        content = self._getFileContent(path)
        title = self._chop(os.path.basename(path), self.extension)
        obj = re.search(r'^#{1}\s{1}(.*)', content, re.MULTILINE | re.UNICODE)
        if obj is not None:
            title = obj.group(1) if len(re.findall(r'\{.*\}', obj.group(1))) == 0 else title
        # return title.encode('ascii', 'ignore').decode('ascii')
        return title

    @staticmethod
    def _chop(theString: str, ext: str) -> str:
        if theString.endswith(ext):
            return theString[:-len(ext)]
        return theString

    def getFileMeta(self, path: str, item: str) -> str:
        """
        Get file meta data of given file

        Args:

            path (str): file path
            item (str): meta data name

        Returns:

            item str(): Metadata of the file
        """
        # os.stat_float_times(True)
        file_stats = os.stat(path)
        switch = {
            'ctime': file_stats.st_birthtime,
            'mtime': file_stats.st_mtime,
            'size': file_stats.st_size
        }
        return switch[item]

    def getFilesListSorted(self, reverse: bool = True) -> list:
        """
        Get list of files in directory as dict

        Args:

            reverse (boolean): True to sort reverse

        Returns:

            list(dict): sorted dict with file meta information
        """
        err = 0
        file_list = list()
        try:
            file_list = os.listdir(self.path)
            # file_list = os.walk(self.path)
        except OSError as e:
            err = e.errno
            pass
        if err == 0:
            seq = list()
            for f in file_list:
                f_path = os.path.join(self.path, f)
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

    def tagSearch(self, tag, sort_by: str = 'tag', reverse: bool = False) -> list:
        """
        Search for notes with tag

        Args:

            tag (str): tag to search for in a note
            sort_by (str, optional): Sort results by. Defaults to 'tag'.
            reverse (bool, optional): Sort reverse. Defaults to False.

        Returns:

            list(dict): results list with dicts

        """
        i = {'tag': 0, 'count': 1}
        matches = list()
        sorted_file_list = self.getFilesListSorted()
        regex = re.compile(
            r'#{1}(\w+)\s?', re.I) if tag == '' else re.compile(r'#{1}(' + tag + r'\w*)\s?', re.I | re.UNICODE)
        for f in sorted_file_list:
            content = self._getFileContent(f['path'])
            if content != str():
                if self.search_yaml_tags_only:
                    match_obj = re.search(r'\bTags:.*', content, re.IGNORECASE | re.UNICODE)
                    if match_obj:
                        r = match_obj.group(0)
                        results = re.findall(regex, r)
                        matches.extend(results)
                else:
                    results = re.findall(regex, content)
                    matches.extend(results)

        counted_matches = Counter([v.lower() for v in matches])
        # Sorted by match counter x[1] if sort by key (tag name) is required change to x[0]
        sorted_matches = OrderedDict(
            sorted(counted_matches.items(), key=lambda x: x[i[sort_by]], reverse=reverse))
        return sorted_matches

    def todoSearch(self, todo: str) -> list:
        """
        Search for todos in md notes

        Args:

            todo (str): Search string

        Returns:

            list(dict): returns matches as list with dict
        """
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
                        'todo': i.replace("*", ""),
                        'filename': f['filename'],
                        'title': f['title'],
                        'mtime': self.getFileMeta(f['path'], 'mtime'),
                        'ctime': self.getFileMeta(f['path'], 'ctime')
                    }
                    matches.append(r_dict)
        ret_list_dict = sorted(matches, key=lambda k: k['mtime'], reverse=self.todo_newest_oldest)
        return ret_list_dict

    def _getFileContent(self, file_path: str) -> str:
        """
        Read file content from md/txt file

        Args:

            file_path (str): Path to file to read

        Returns:

            str: content
        """
        if str(file_path).endswith(self.extension):
            with open(file_path, 'r') as c:
                content = c.read()
        else:
            content = str()
        return content

    def isNoteTagged(self, file_path: str, tag: str) -> bool:
        """
        Is the note tagged with tag?

        Args:

            file_path (str): path to note
            tag (str): tag to search for

        Returns:
            boolean: True if note is tagged otherwise false
        """
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
    def get_search_config(q: str) -> tuple:
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
        elif q == str():
            s_terms = list()
            s_type = 'or'
        else:
            s_terms = [q]
            s_type = 'or'
        return s_terms, s_type

    def getUrlScheme(self, f: str) -> str:
        """
        Gets the URL Scheme setup in Alfred Preferences

        Args:
            f(str): md file to add at the end of url scheme

        Returns:
            str: URL scheme
        """
        return self.strJoin(self.url_scheme, pathname2url(f))


class NewNote(Notes):
    """
    Creates a new note with title, template and tags

    Args:

        note_title (str): Title of the Note
        template_path (str): Path to the template used
        tags (str): Tag line with format: #tag1 #tag2
        content (str): Addtional content after Headline

    """

    def __init__(self, note_title, template_path=str(), tags=str(), content=str()):
        super(NewNote, self).__init__()
        self.filename_format = self.getFilenameFormat()
        self.tags = tags
        self.content = content
        self.note_title = note_title
        self.note_path = self.getTargetFilePath(self.__normalize_filename(note_title))
        self.template_path = self.getTemplate(template_path)

    def getFilenameFormat(self):
        """
        Get fileformat from WF env

        Returns:

            str: fileformat or fallback
        """
        frmt_env = Tools.getEnv('filename_format')
        if frmt_env is None or frmt_env.strip() == "":
            frmt_env = '{title}'
        return frmt_env

    def getTargetFilePath(self, file_name: str) -> str:
        """
        construct markdown file path

        Returns:

            str: markdown file path
        """
        def applyFilenameFormat(title: str):
            """Appliies configured Fileformat to filename"""
            frmt = self.filename_format
            res = re.findall(r"\{[\.\-:%a-zA-Z]*\}", frmt)
            for r in res:
                if "%" in r:
                    date_f = r.replace('{', "").replace('}', "")
                    dte = self.getTodayDate(date_f)
                    frmt = frmt.replace(r, dte)
                elif '{title}' in res:
                    frmt = frmt.replace(r, title)
            return frmt

        file_name = file_name.rstrip().lstrip()
        file_name = applyFilenameFormat(file_name)
        file_path = os.path.join(self.path, f"{file_name}{self.extension}")
        if os.path.isfile(file_path):
            new_file_name = Tools.strJoin(file_name, ' ', self.getTodayDate('%d-%m-%Y %H-%M-%S'))
            file_path = os.path.join(self.path, f"{new_file_name}{self.extension}")
        return file_path

    def getDefaultTemplate(self) -> str:
        """
        Read default template setting from environment variable

        Returns:

            str: default template file name
        """
        return 'template.md' if self.default_template == str() else self.default_template

    def getTemplate(self, template_path: str) -> str:
        """
        Get template path from previous wf step, reads env variable

        Returns:

            str: path to template.md
        """
        notes_path = self.path
        default_template = self.getDefaultTemplate()
        return os.path.join(notes_path, default_template) if template_path == str() else template_path

    def readTemplate(self, **kwargs: str) -> str:
        """
        Read template mardkown file and fill placeholder defined in template
        with data provides as kwargs

        Args:

            file_path (str): Path to Template file

        Returns:

            str: Content
        """
        if '#' not in self.template_tag or self.template_tag == str():
            self.template_tag = '#Template'
        if os.path.exists(self.template_path):
            with open(self.template_path, "r") as f:
                content = f.read()
        else:
            content = self.FALLBACK_CONTENT
        content = content.replace(self.template_tag, '')
        for k, v in kwargs.items():
            content = content.replace('{' + k + '}', v)
        tag_line = f'Tags: {self.tags}'
        if self.tags:
            content = content.replace('Tags: ', tag_line)
        return content

    def __normalize_filename(self, f: str) -> str:
        """
        Replace special characters in filename of md file

        Returns:

            str: filename
        """
        return self.strReplace(f, self.CHAR_REPLACEMENT_MAP, lowercase=False)

    def createNote(self) -> str:
        """
        Creates the markdown note

        Returns:

            str: full path to notes
        """
        try:
            with open(self.note_path, "w+") as f:
                default_date = self.getDefaultDate()
                file_content = self.readTemplate(
                    date=self.getTodayDate(default_date), title=self.note_title)
                file_content = f"{file_content}\n{self.content}" if self.content else file_content
                f.write(file_content)
            return self.note_path
        except IOError as e:
            sys.stderr.write(e)
