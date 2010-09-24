"""
ZCML registrations.
"""
from zope import interface
from zope.component import getUtility
from zope.configuration.fields import Path
from collective.amberjack.core.interfaces import ITourRegistration

import os

class ITourDirective(interface.Interface):
    """Create tour registration."""

    tourlocation = Path(
        title=u'Location where you placed the tour',
        description=u'The variable that points to the tour',
        required=True)

def _registerTour(source, filename):
    reg = getUtility(ITourRegistration, 'zipfile')
    registration = reg(source, filename=filename)
    registration.register()

def tour(_context, tourlocation):
    """Tour class factory registration."""
    archive = open(tourlocation,'r')
    archive.seek(0)
    source = archive.read()
    archive.close()
    filename = os.path.basename(tourlocation)
    _context.action(
        discriminator = '_registerTour:%s' % tourlocation,
        callable = _registerTour,
        args = (source, filename)
    )

