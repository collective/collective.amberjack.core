from zope.interface import classProvides
from zope.component import provideUtility
from collective.amberjack.core.interfaces import ITourDefinition
from collective.amberjack.core.experimental.interfaces import ITourRegistration
from collective.amberjack.core.experimental.tour import Tour
import zipfile
import os

class TourRegistration(object):
    """
    Generic tour registration class
    """
    classProvides(ITourRegistration)

    def __init__(self, uri):
        self.uri = uri

    def source_packages(self):
        raise NotImplemented

    def tour_namespace(self):
        raise NotImplemented

    def register(self):
        for conf in self.source_packages():
            tour = Tour(conf, self.tour_namespace())
            provideUtility(component=tour, 
                           provides=ITourDefinition,
                           name=tour.tourId)
    def isProperTour(self, filename):
        return filename.endswith(".cfg")

class FileArchiveRegistration(TourRegistration):
    """
    Zip archive tour registration
    """
    classProvides(ITourRegistration)

    def source_packages(self):
        self.archive = zipfile.ZipFile(self.uri, "r")
        for f in self.archive.namelist():
            if not self.isProperTour(f):
                continue
            yield self.archive.open(f,'r')

    def tour_namespace(self):
        return os.path.basename(self.archive.filename)
