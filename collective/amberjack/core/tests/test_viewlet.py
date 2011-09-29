import os
import unittest

import zope.component
from zope.component import getUtility

import plone.i18n.normalizer
from Zope2.App import zcml

import collective.amberjack.core
import collective.amberjack.core.tests
from collective.amberjack.core.tests.base import AmberjackCoreTestCase
from collective.amberjack.core.viewlets.tour import TourViewlet
from collective.amberjack.core.interfaces import ITourRegistration
from collective.amberjack.core.interfaces import ITourManager


class TourViewletTestCase(AmberjackCoreTestCase):

    def afterSetUp(self):
        self.test_folder = os.path.dirname(
                collective.amberjack.core.tests.__file__)
        archive_path = os.path.join(self.test_folder, 'basic_tours.zip')

        archive = open(archive_path, 'r')
        archive.seek(0)
        source = archive.read()
        archive.close()
        filename = os.path.basename(archive_path)
        
        zcml.load_config('meta.zcml', zope.component)
        zcml.load_config('meta.zcml', collective.amberjack.core)
        zcml.load_config('configure.zcml', collective.amberjack.core)
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
        <utility component="collective.amberjack.core.registration.FileArchiveRegistration"
                 name="zip_archive" />
        </configure>''')

        filename = os.path.dirname(collective.amberjack.core.tests.__file__)
        zcml_string = '''<configure
        xmlns="http://namespaces.zope.org/zope"
        xmlns:collective.amberjack="http://namespaces.plone.org/collective.amberjack.core">
        <collective.amberjack:tour
             tourlocation="%s/basic_tours.zip"
        />
        </configure>''' % filename
        zcml.load_string(zcml_string)
        reg = zope.component.queryUtility(ITourRegistration, 'zip_archive')
        registration = reg(source, filename)
        registration.register()
        
        self.context = self.portal
        
        manager = getUtility(ITourManager)
        manager.getTours(self.context)

    def test_viewlet_renderer(self):

        self.portal.REQUEST.set('tourId', '01_basic_add_and_publish_a_folder-add-and-publish')
        viewlet = TourViewlet(self.portal, self.portal.REQUEST, None, None)
        viewlet.update()
        viewlet.render()


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TourViewletTestCase))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
