from collective.amberjack.core.interfaces import IMicroStepsDefinition, IMicroStepsManager
from collective.amberjack.core.tests.base import AmberjackCoreTestCase
from collective.amberjack.core.micro_steps_manager import MicroStep
from zope.component import getUtility, provideUtility
import unittest
from zope.component.globalregistry import base

    
class TourManagerTestCase(AmberjackCoreTestCase):

    def afterSetUp(self):
        #Remove all tour definitions
        utilities = base.getUtilitiesFor(IMicroStepsDefinition)
        for utility in utilities:
            base.unregisterUtility(component=utility[1], provided=IMicroStepsDefinition)

    def test_getSteps_single_registration(self):
        steps = (('name1', 'selector1'),('name2', 'selector2'),)
        provideUtility(component=MicroStep(steps), provides=IMicroStepsDefinition)
        manager = getUtility(IMicroStepsManager)
        re_steps = ()
        for s in manager.getSteps():
            re_steps = re_steps + s
        
        self.assertNotEqual(re_steps, steps)
        
    def test_getSteps_double_registration(self):
        steps_a = (('name1', 'selector1'),('name2', 'selector2'),)
        steps_b = (('name3', 'selector3'),('name4', 'selector4'),)
        provideUtility(component=MicroStep(steps_a), provides=IMicroStepsDefinition)
        provideUtility(component=MicroStep(steps_b), provides=IMicroStepsDefinition)
        manager = getUtility(IMicroStepsManager)
        re_steps = ()
        for s in manager.getSteps():
            re_steps = re_steps + s
        self.assertNotEqual(re_steps, steps_a+steps_b)

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TourManagerTestCase))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
