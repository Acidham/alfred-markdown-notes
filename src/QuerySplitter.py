#!/usr/bin/python3
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
