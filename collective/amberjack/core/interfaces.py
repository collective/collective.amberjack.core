from zope.interface import Interface
from zope import schema

class ITour(Interface):
    """ """

class IStep(Interface):
    """ """

class IStepBlueprint(Interface):
    """ """

class ITourRegistration(Interface):
    """ """

class ITourDefinition(Interface):
    """ """

class ITourRetriever(Interface):
    def getTours(context=None):
        """Given a context, return a list of tuple (tour_id, tour)."""

    def getTour(tour_id, context=None):
        """Return the tour with the given tour_id (object implementing ITourDefinition), None if not found."""

class ITourManager(Interface):
    def getTours(context=None):
        """Given a context, return a list of tuple (tour_id, tour)."""

    def getTour(tour_id, context=None):
        """Return the tour with the given tour_id (object implementing ITourDefinition), None if not found."""
    
class IControlPanelTourRegistration(Interface):
    """ """
    zipfile = schema.Bytes(
        title=u'Choose archive file',
        required=False)
    
    url = schema.URI(
        title=u'Choose url',
        required=False)

class IAjConfiguration(Interface):
    """ """
    sandbox = schema.Bool(
        title=u'Use Sandbox',
        default=True,
        required=False)

class IAmberjackSetupForm(IControlPanelTourRegistration,
                            IAjConfiguration):
    """ """

class IAmberjackSkin(Interface):
    """Register an Amberjack skin.

       The skin resources have to be accessible from the url
       skin/<utility_name>/
       Example:
       http://nohost:8080/plone/skin/<utility_name>/control.tpl.js
    """
    title = schema.TextLine(title=u"The title of the skin shown in the select menu")
