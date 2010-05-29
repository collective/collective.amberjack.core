from collective.amberjack.core.tests.base import AmberjackCoreTestCase
from collective.amberjack.core.experimental.viewlet import TourViewlet
from collective.amberjack.core.experimental.interfaces import ITourRegistration
from zope.component import getUtility

import os
import unittest
import collective.amberjack.core.tests

class TourViewletTestCase(AmberjackCoreTestCase):

    def afterSetUp(self):
        self.test_folder = os.path.dirname(collective.amberjack.core.tests.__file__)
        reg = getUtility(ITourRegistration, 'zip_archive')
        registration = reg(os.path.join(self.test_folder, 'basic_tours.zip'))
        registration.register()

    def test_viewlet_renderer(self):
        self.portal.REQUEST.set('tourId', 'basic_tours-zip-add-and-publish-a-folder')
        viewlet = TourViewlet(self.portal, self.portal.REQUEST, None, None)
        viewlet.update()
        viewlet.render()

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TourViewletTestCase))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
