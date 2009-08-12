from collective.amberjack.core.interfaces import ITourDefinition
from zope.interface import implements


class Tour(object):
    implements(ITourDefinition)
    
    def __init__(self, ajTour):
        self.tour = ajTour

    def tourId(self):
        """Return the tourId."""
        return self.tour['tourId']

    def title(self):
        """Return the title."""
        return self.tour['title']
    
    def steps(self):
        """Return a dict:
        {'url': 'url',
         'xpath': 'xpath expression',
         'xcontent': 'xcontent',
         'title': 'title',
         'text': 'text',
         'steps': ((description, idStep, selector, text), ...)}

        """
        return self.tour['steps']
