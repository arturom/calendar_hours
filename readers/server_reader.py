from httplib2 import Http
from icalevents.icaldownload import ICalDownload

from .reader import Reader

class ServerReader(Reader):
    def __init(self, url):
        self.url = url

    def read(self):
        http = Http(".cache")
        return ICalDownload(http).data_from_url(self.url)
