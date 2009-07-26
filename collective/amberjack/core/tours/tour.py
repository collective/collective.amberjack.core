from zope.interface import implements
from collective.amberjack.core.interfaces import ITourDefinition
from zope.component import getMultiAdapter

class Tour:
    implements(ITourDefinition)
    
    def __init__(self, ajTour):
        self.tour = ajTour
        
    