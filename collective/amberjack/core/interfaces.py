from zope.interface import Interface


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

