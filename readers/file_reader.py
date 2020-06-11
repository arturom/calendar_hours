from icalevents.icaldownload import ICalDownload

from .reader import Reader


class FileReader(Reader):
    def __init__(self, filepath):
        self.filepath = filepath

    def read(self):
        return ICalDownload(None).data_from_file(self.filepath)
