"""
ZCML registrations.
"""
from zope import interface
from zope.configuration.fields import GlobalObject
from collective.amberjack.core.tours.tour import Tour
from collective.amberjack.core.tour_manager import registerTour


class ITourDirective(interface.Interface):
    """Create tour registration."""
    tourdescriptor = GlobalObject(
        title=u'Tour descriptor',
        description=u'The variable that describes the tour',
        required=True)


def tour(_context, tourdescriptor, **kwargs):
    """Tour class factory registration."""
    registerTour(Tour(tourdescriptor))
