from urlparse import urlparse

from django.core.urlresolvers import resolve


class URLString(object):
    def __init__(self, url_string):
        self.url_string = url_string
        self.url = urlparse(self.url_string)

    def resolve(self):
        return resolve(self.url.path)
