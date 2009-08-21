"""
ZCML registrations.
"""
from collective.amberjack.core.interfaces import ITourDefinition
from collective.amberjack.core.tour import Tour
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
