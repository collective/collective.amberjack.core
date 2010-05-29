from zope.interface import classProvides
from zope.component import provideUtility
from collective.amberjack.core.interfaces import ITourDefinition
from collective.amberjack.core.experimental.interfaces import ITourRegistration
from collective.amberjack.core.experimental.tour import Tour
import zipfile
from cStringIO import StringIO
import urllib2
import os
from urlparse import urlparse

class TourRegistration(object):
    """
    Generic tour registration class
    """
    classProvides(ITourRegistration)

    def __init__(self, source, request):
        self.source = source
        self.request = request

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

    # BBB: other archives

    def source_packages(self):
        _zip = StringIO()
        _zip.write(self.source)
        self.archive = zipfile.ZipFile(_zip)
        for f in self.archive.namelist():
            if not self.isProperTour(f):
                continue
            yield self.archive.open(f,'r')

    def tour_namespace(self):
        return self.request.form['form.zipfile'].filename

class WebRegistration(TourRegistration):
    """
    Web tour registration
    """
    classProvides(ITourRegistration)

    # BBB: other archives

    def source_packages(self):
        response = urllib2.urlopen(self.source)
        _zip = StringIO()
        _zip.write(response.read())
        self.archive = zipfile.ZipFile(_zip)
        for f in self.archive.namelist():
            if not self.isProperTour(f):
                continue
            yield self.archive.open(f,'r')

    def tour_namespace(self):
        return os.path.basename(urlparse(self.request.form['form.url']).path)
