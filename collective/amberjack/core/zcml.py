"""
ZCML registratins.
"""
from zope import interface
from zope.configuration.fields import GlobalObject
from collective.amberjack.core.tours.tour import Tour
from collective.amberjack.core.tour_manager import registerTour

class ITourDirective( interface.Interface ):
    """ Creates tour registrtion"""
    
    tourdescriptor = GlobalObject(
        title=u'Tour descriptor',
        description=u'The variable that describes the tour',
        required=True)


def tour(_context, tourdescriptor, **kwargs):
    """ tour class factory registration."""
    registerTour(Tour(tourdescriptor))
