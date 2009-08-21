from zope.interface import Interface
from zope.schema import TextLine


class IAmberjackSkin(Interface):
    """Register an Amberjack skin.

       The skin resources have to be accessible from the url
       skin/<utility_name>/
       Example:
       http://nohost:8080/plone/skin/<utility_name>/control.tpl.js
    """
    title = TextLine(title=u"The title of the skin shown in the select menu")


class ITourDefinition(Interface):
    def tourId():
        """Return the tourId."""

    def title():
        """Return the title."""
    
    def steps():
        """Return a dict:
        {'url': 'url',
         'xpath': 'xpath expression',
         'xcontent': 'xcontent',
         'title': 'title',
         'text': 'text',
         'steps': ((description, idStep, selector, text), ...)}

        """


class ITourRetriever(Interface):
    def getTours(context=None):
        """Given a context, return a list of tuple (tour_id, title)."""

    def getTour(tour_id, context=None):
        """Return the tour with the given tour_id (object implementing ITourDefinition), None if not found."""


class IManageTourUtility(Interface):
    def getTours(context=None):
        """Given a context, return a list of tuple (tour_id, title)."""

    def getTour(tour_id, context=None):
        """Return the tour with the given tour_id (object implementing ITourDefinition), None if not found."""

