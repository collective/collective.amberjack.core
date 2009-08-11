from zope.interface import Interface


class ITourDefinition(Interface):
    def tourId():
        """Return the tourId."""

    def title(self):
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

