from unittest import defaultTestLoader, main
from zope.component import queryUtility, getUtility
from collective.amberjack.core.experimental.interfaces import ITourRegistration
from collective.amberjack.core.interfaces import ITourDefinition
from Testing import ZopeTestCase as ztc
from Products.Five import zcml
import os

import zope.component
import plone.i18n.normalizer
import collective.amberjack.core.tests

class RegistrationTests(ztc.ZopeTestCase):

    def setUp(self):
        self.test_folder = os.path.dirname(collective.amberjack.core.tests.__file__)
        zcml.load_config('meta.zcml', zope.component)
        zcml.load_config('configure.zcml', plone.i18n.normalizer)
        zcml.load_string('''<configure
        xmlns="http://namespaces.zope.org/zope">
        <utility component="collective.amberjack.core.experimental.blueprints.Step"
                 name="collective.amberjack.blueprints.step" />
        </configure>''')

        zcml.load_string('''<configure
        xmlns="http://namespaces.zope.org/zope">
        <utility component="collective.amberjack.core.experimental.blueprints.MicroStep"
                 name="collective.amberjack.blueprints.microstep" />
        </configure>''')

        zcml.load_string('''<configure
        xmlns="http://namespaces.zope.org/zope">
        <utility component="collective.amberjack.core.experimental.registration.FileArchiveRegistration"
                 name="zip_archive" />
        </configure>''')

    def test_register_zip(self):
        reg = queryUtility(ITourRegistration, 'zip_archive')
        registration = reg(os.path.join(self.test_folder, 'basic_tours.zip'))
        registration.register()
        tour = getUtility(ITourDefinition, u'basic_tours-zip-add-and-publish-a-folder')
        self.assertEqual(tour.tourId, 'basic_tours-zip-add-and-publish-a-folder')

def test_suite():
    return defaultTestLoader.loadTestsFromName(__name__)

if __name__ == '__main__':
    main(defaultTest='test_suite')
