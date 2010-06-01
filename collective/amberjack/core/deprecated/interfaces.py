from zope.interface import Interface
from zope import schema
from zope.configuration.fields import GlobalObject, Path


class IStepDefinition(Interface):
    
    url = Path(title=u'Step url', required=True)
     
    xpath = schema.TextLine(title=u'XPath', required=True) 
    
    xcontent = schema.TextLine(title=u'XContent', required=True)
    
    title = schema.TextLine(title=u'Title', required=True)
    
    text = schema.TextLine(title=u'Text', required=True) 

    steps = schema.Tuple(title=u'Step micro steps', 
                         required=True)

    validators = schema.Tuple(value_type=GlobalObject(title=u'Precondition callable',
        description=u'Should return None if the precondition is satisfied, else an error message.',
        ),
        required=False)

    def validate(context, request):
        """Return an empty list if the step can be started,
        else a list of errors."""

class ITourDefinition(Interface):
    
    tourId = schema.TextLine(title=u'Tour proper id', 
                             required=True)
    
    title = schema.TextLine(title=u'Tour proper title', 
                            required=True)
    
    steps = schema.Tuple(title=u'Tour steps', 
                         required=True)

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
    
class IMicroStepsManager(Interface):
    def addStepsDefinition(steps):
        """add a tuple of steps' definition to the registry"""
        
    def getSteps():
        """returns the list of all the registered microsteps"""

