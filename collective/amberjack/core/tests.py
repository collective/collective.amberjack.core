import unittest

from zope.testing import doctestunit
from zope.component import testing
from Testing import ZopeTestCase as ztc

from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite
ptc.setupPloneSite()

import collective.amberjack.core
from collective.amberjack.core.interfaces import IManageTourUtility

from zope.component import getUtility


class TestCase(ptc.PloneTestCase):
    class layer(PloneSite):
        @classmethod
        def setUp(cls):
            fiveconfigure.debug_mode = True
            zcml.load_config('configure.zcml',
                             collective.amberjack.core)
            fiveconfigure.debug_mode = False

        @classmethod
        def tearDown(cls):
            pass

    def test_register_utility_available(self):
        register = getUtility(IManageTourUtility)
        
    def test_register_tour(self):
        register = getUtility(IManageTourUtility)
        tour = 'tour1'
        register.add(tour)
        self.assertEqual(register.getTours(), [tour,])


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestCase))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
