import os
from unittest import defaultTestLoader, main

from zope.component import queryUtility, getUtility
import zope.component

import plone.i18n.normalizer
from Testing import ZopeTestCase as ztc
from Zope2.App import zcml

from collective.amberjack.core.interfaces import ITourRegistration
from collective.amberjack.core.interfaces import ITourDefinition
import collective.amberjack.core.tests


class RegistrationTests(ztc.ZopeTestCase):

    def setUp(self):
        self.test_folder = os.path.dirname(collective.amberjack.core.tests.__file__)
        zcml.load_config('meta.zcml', zope.component)
        zcml.load_config('configure.zcml', plone.i18n.normalizer)
        zcml.load_string('''<configure
        xmlns="http://namespaces.zope.org/zope">
        <utility component="collective.amberjack.core.blueprints.Step"
                 name="collective.amberjack.blueprints.step" />
        </configure>''')

        zcml.load_string('''<configure
        xmlns="http://namespaces.zope.org/zope">
        <utility component="collective.amberjack.core.blueprints.MicroStep"
                 name="collective.amberjack.blueprints.microstep" />
        </configure>''')
        
        zcml.load_string('''<configure
        xmlns="http://namespaces.zope.org/zope">
        <utility component="collective.amberjack.core.blueprints.WindmillMicroStep"
                 name="collective.amberjack.blueprints.windmillmicrostep" />
        </configure>''')

        zcml.load_string('''<configure
        xmlns="http://namespaces.zope.org/zope">
        <utility component="collective.amberjack.core.registration.FileArchiveRegistration"
                 name="zip_archive" />
        </configure>''')
        
    def test_register_tar_gz(self):
        reg = queryUtility(ITourRegistration, 'zip_archive')
        archive_path = os.path.join(self.test_folder, 'basic_tours.tar.gz')
        archive = open(archive_path, 'r')
        archive.seek(0)
        source = archive.read()
        archive.close()
        filename = os.path.basename(archive_path)
        registration = reg(source, filename)
        registration.register()
        tour = getUtility(ITourDefinition, u'01_basic_add_and_publish_a_folder-add-and-publish')
        self.assertEqual(tour.tourId, '01_basic_add_and_publish_a_folder-add-and-publish')
        
    def test_register_tar(self):
        reg = queryUtility(ITourRegistration, 'zip_archive')
        archive_path = os.path.join(self.test_folder, 'basic_tours.tar')
        archive = open(archive_path, 'r')
        archive.seek(0)
        source = archive.read()
        archive.close()
        filename = os.path.basename(archive_path)
        registration = reg(source, filename)
        registration.register()
        tour = getUtility(ITourDefinition, u'01_basic_add_and_publish_a_folder-add-and-publish')
        self.assertEqual(tour.tourId, '01_basic_add_and_publish_a_folder-add-and-publish')
    
    def test_register_zip(self):
        reg = queryUtility(ITourRegistration, 'zip_archive')
        archive_path = os.path.join(self.test_folder, 'basic_tours.zip')
        archive = open(archive_path, 'r')
        archive.seek(0)
        source = archive.read()
        archive.close()
        filename = os.path.basename(archive_path)
        registration = reg(source, filename)
        registration.register()
        tour = getUtility(ITourDefinition, u'01_basic_add_and_publish_a_folder-add-and-publish')
        self.assertEqual(tour.tourId, '01_basic_add_and_publish_a_folder-add-and-publish')
        

def test_suite():
    return defaultTestLoader.loadTestsFromName(__name__)


if __name__ == '__main__':
    main(defaultTest='test_suite')
