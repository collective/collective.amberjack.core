from zope.interface import classProvides
from zope.component import provideUtility
from collective.amberjack.core.interfaces import ITourDefinition
from collective.amberjack.core.experimental.interfaces import ITourRegistration
from collective.amberjack.core.experimental.tour import Tour
import zipfile
import tarfile
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


def archive_handler(filename, source):
    """ yield extracted files from a archive """

    source.seek(0)

    if filename.endswith('.zip'):
        #ZIP
        _zip = zipfile.ZipFile(source)
        for f in _zip.namelist():
            yield f, _zip.open(f,'r')
        
    elif filename.endswith('.tar'):
        #TAR
        _tar = tarfile.TarFile.open(fileobj=source, mode='r:')
        for f in _tar.getmembers():
            extract = _tar.extractfile(f)
            if extract:
                yield extract.name, extract

    elif filename.endswith('.gz'):
        #GZ
        _tar = tarfile.TarFile.open(fileobj=source, mode='r:gz')
        for f in _tar.getmembers():
            extract = _tar.extractfile(f)
            if extract:
                yield extract.name, extract

class FileArchiveRegistration(TourRegistration):
    """
    Zip archive tour registration
    """
    classProvides(ITourRegistration)

    def source_packages(self):
        _zip = StringIO()
        _zip.write(self.source)
        for filename, archive in archive_handler(self.tour_namespace(), _zip):
            if not self.isProperTour(filename):
                continue
            yield archive

    def tour_namespace(self):
        return self.request.form['form.zipfile'].filename

class WebRegistration(TourRegistration):
    """
    Web tour registration
    """
    classProvides(ITourRegistration)

    def source_packages(self):
        response = urllib2.urlopen(self.source)
        _zip = StringIO()
        _zip.write(response.read())
        for filename, archive in archive_handler(self.tour_namespace(), _zip):
            if not self.isProperTour(filename):
                continue
            yield archive

    def tour_namespace(self):
        return os.path.basename(urlparse(self.request.form['form.url']).path)



