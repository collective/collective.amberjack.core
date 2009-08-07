from collective.amberjack.core.interfaces import ITourDefinition
from zope.interface import implements


class Tour(object):
    implements(ITourDefinition)
    
    def __init__(self, ajTour):
        self.tour = ajTour
        
    
