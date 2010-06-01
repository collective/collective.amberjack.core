"""
ZCML registrations.
"""
from zope.component import provideUtility
from plone.registry import Record
from plone.registry import field
from zope import interface
from zope.component import getUtility
from zope.configuration.fields import GlobalObject
from zope.configuration.fields import Path
from collective.amberjack.core.interfaces import ITourRegistration
from collective.amberjack.core.deprecated.micro_steps_manager import registry
from collective.amberjack.core.deprecated.tour import Tour as OldTour
from collective.amberjack.core.deprecated.interfaces import ITourDefinition

import os

class ITourDirective(interface.Interface):
    """Create tour registration."""

    tourdescriptor = GlobalObject(
            title=u'Tour descriptor',
            description=u'The variable that describes the tour',
            required=False)

    tourlocation = Path(
        title=u'Location where you placed the tour',
        description=u'The variable that points to the tour',
        required=False)

def _registerTour(source, filename):
    reg = getUtility(ITourRegistration, 'zipfile')
    registration = reg(source, filename=filename)
    registration.register()

def _deprecatedRegisterTour(tourdescriptor):
    tour = OldTour(**tourdescriptor)
    provideUtility(component=tour,
                       provides=ITourDefinition,
                       name=tour.tourId)

def tour(_context, tourdescriptor=None, tourlocation=None):
    """Tour class factory registration."""
    if tourdescriptor:
        _deprecatedRegisterTour(tourdescriptor)
    elif tourlocation:
        archive = open(tourlocation,'r')
        archive.seek(0)
        source = archive.read()
        archive.close()
        filename = os.path.basename(tourlocation)
        _context.action(
            discriminator = '_registerTour',
            callable = _registerTour,
            args = (source, filename)
        )
    else:
        raise AttributeError('You need to provide tourdescriptor or tourlocation.')


class IStepDirective(interface.Interface):
    """Create a ajStep registration"""
    stepsdescriptor = GlobalObject(
        title=u'Steps set',
        description=u'The variable that identifies a set of steps',
        required=True)

def ajstep(_context, stepsdescriptor):
    if not 'collective.amberjack.core.microsteps' in registry:
        microsteps = field.Tuple(title=u'microstep')
        record_microstep = Record(microsteps)
        record_microstep.value = stepsdescriptor
        registry.records['collective.amberjack.core.microsteps'] = record_microstep
    else:
        registry.records['collective.mberjack.core.microsteps'].value += stepsdescriptor
