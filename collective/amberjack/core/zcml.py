"""
ZCML registrations.
"""
from collective.amberjack.core.interfaces import ITourDefinition
from collective.amberjack.core.interfaces import IMicroStepsDefinition
from collective.amberjack.core.tour import Tour
from collective.amberjack.core.micro_steps_manager import MicroStep
from zope import interface
from zope.component import provideUtility
from zope.configuration.fields import GlobalObject



class ITourDirective(interface.Interface):
    """Create tour registration."""
    tourdescriptor = GlobalObject(
        title=u'Tour descriptor',
        description=u'The variable that describes the tour',
        required=True)


def tour(_context, tourdescriptor, **kwargs):
    """Tour class factory registration."""
    tour = Tour(**tourdescriptor)
    provideUtility(component=tour, 
                   provides=ITourDefinition,
                   name=tour.tourId)

class IStepDirective(interface.Interface):
    """Create a ajStep registration"""
    stepsdescriptor = GlobalObject(
        title=u'Steps set',
        description=u'The variable that identifies a set of steps',
        required=True)
    
def ajstep(_context, stepsdescriptor):
    provideUtility(component=MicroStep(stepsdescriptor), 
                   provides=IMicroStepsDefinition)