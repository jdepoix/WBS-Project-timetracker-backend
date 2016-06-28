from urlparse import urlparse

from django.core.urlresolvers import resolve


class URLString(object):
    """
    wraps a url string to add functionallity and retrieve information needed
    """
    def __init__(self, url_string):
        """
        initialized with the url string

        :param url_string: the url as string
        :type url_string: str
        """
        self.url_string = url_string
        self.url = urlparse(self.url_string)

    def resolve(self):
        """
        resolves the string using djangos resolve method
        :return: resolved url
        :rtype: ResolverMatch
        """
        return resolve(self.url.path)
