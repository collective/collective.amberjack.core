from collective.amberjack.core.interfaces import ITourManager, \
    ITourDefinition, ITourRetriever
from collective.amberjack.core.tests.base import AmberjackCoreTestCase
from collective.amberjack.core.tour import Tour
from zope.component import getUtility, provideUtility
from collective.amberjack.core.validators import isAnonymous, isAuthenticated
import unittest
from zope.component.globalregistry import base

def isNotVisibleStep(context):
    return False

def registerTour(tour=None):
    if not tour:
        tour = {'tourId': u'dummy_id',
                'title': u'Dummy title',
                'steps': ({'url': u'/opt/var',
                           'xpath': u'xpath expression',
                           'xcontent': u'xcontent',
                           'title': u'title',
                           'text': u'text',
                           'steps': ()},
                           ),}
    tour = Tour(**tour) 
    provideUtility(component=tour, provides=ITourDefinition, name=tour.tourId)
    
class TourManagerTestCase(AmberjackCoreTestCase):

    def afterSetUp(self):
        #Remove all tour definitions
        utilities = base.getUtilitiesFor(ITourDefinition)
        for utility in utilities:
            base.unregisterUtility(component=utility[1], provided=ITourDefinition, name=utility[0])        

    def test_getTours(self):
        registerTour()
        manager = getUtility(ITourManager)
        self.assertEqual(manager.getTours(self.portal),[(u'dummy_id', u'Dummy title')])
        
    def test_getTour(self):      
        registerTour()
        manager = getUtility(ITourManager)
        self.assertEqual(manager.getTour('dummy_id', self.portal).tourId, 'dummy_id')
                         
    def test_PackagedTourRetriever(self):
        registerTour()
        managetour = getUtility(ITourManager)
        packagetour = getUtility(ITourRetriever, name='retriever.packagedtours')        
        self.assertEqual(managetour.getTours(self.portal), packagetour.getTours(self.portal))

    def test_multiple_same_tours(self):
        [registerTour() for a in range(10)]
        registerTour({'tourId': u'dummy_id',
                     'title': u'Last tour title',
                     'steps': ({'url': u'/opt/var',
                                'xpath': u'xpath expression',
                                'xcontent': u'xcontent',
                                'title': u'title',
                                'text': u'text',
                                'steps': ()
                                },),
                     })
        managetour = getUtility(ITourManager)
        self.assertEqual(len(managetour.getTours(self.portal)), 1)
        self.assertEqual(managetour.getTours(self.portal)[0][1], u'Last tour title')

    def test_steps_preconditions(self):
        registerTour({'tourId': u'tour_with_conditions',
                     'title': u'Tour with conditions',
                     'steps': ({'url': u'/opt/var',
                                'xpath': u'xpath expression',
                                'xcontent': u'xcontent',
                                'validation': isNotVisibleStep,
                                'title': u'title',
                                'text': u'text',
                                'steps': ()
                                },),
                     })
        
        managetour = getUtility(ITourManager)
        tour = managetour.getTour('tour_with_conditions', self.portal)
        for step in tour.steps:
            self.assertFalse(step.isVisible(self.portal))

    def test_steps_preconditions2(self):
        registerTour({'tourId': u'tour_with_conditions',
                     'title': u'Tour with conditions',
                     'steps': ({'url': u'/opt/var',
                                'xpath': u'xpath expression',
                                'xcontent': u'xcontent',
                                'title': u'title',
                                'text': u'text',
                                'steps': ()
                                },),
                     })
        
        managetour = getUtility(ITourManager)
        tour = managetour.getTour('tour_with_conditions', self.portal)
        for step in tour.steps:
            self.assertTrue(step.isVisible(self.portal))

    def test_steps_anonymous_validation(self):
        registerTour({'tourId': u'tour_with_conditions',
                     'title': u'Tour with conditions',
                     'steps': ({'url': u'/opt/var',
                                'xpath': u'xpath expression',
                                'xcontent': u'xcontent',
                                'title': u'title',
                                'text': u'text',
                                'steps': (),
                                'validation': isAnonymous,
                                },),
                     })
        
        managetour = getUtility(ITourManager)
        tour = managetour.getTour('tour_with_conditions', self.portal)
        for step in tour.steps:
            self.assertFalse(step.isVisible(self.portal))

    def test_steps_authenticated_validation(self):
        registerTour({'tourId': u'tour_with_conditions',
                     'title': u'Tour with conditions',
                     'steps': ({'url': u'/opt/var',
                                'xpath': u'xpath expression',
                                'xcontent': u'xcontent',
                                'title': u'title',
                                'text': u'text',
                                'steps': (),
                                'validation': isAuthenticated,
                                },),
                     })
        
        managetour = getUtility(ITourManager)
        tour = managetour.getTour('tour_with_conditions', self.portal)
        for step in tour.steps:
            self.assertTrue(step.isVisible(self.portal))

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TourManagerTestCase))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
