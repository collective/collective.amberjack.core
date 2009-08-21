from zope.interface import Interface
from zope import schema
from zope.configuration.fields import Tokens, GlobalObject, Path, PythonIdentifier


class IAmberjackSkin(Interface):
    """Register an Amberjack skin.

       The skin resources have to be accessible from the url
       skin/<utility_name>/
       Example:
       http://nohost:8080/plone/skin/<utility_name>/control.tpl.js
    """
    title = schema.TextLine(title=u"The title of the skin shown in the select menu")


class ITourDefinition(Interface):
    
    tourId = schema.TextLine(title = u'Tour proper id', 
                             required = True)
    
    title = schema.TextLine(title = u'Tour proper title', 
                            required = True)
    
    steps = schema.Tuple(title = u'Tour steps', 
                         required = True)


class IStepDefinition(Interface):
    
    url = Path(title = u'Step url', required = True)
     
    xpath = schema.TextLine(title = u'XPath',required = True) 
    
    xcontent = schema.TextLine(title = u'XContent',required = True)
    
    title = schema.TextLine(title = u'Title',required = True)
    
    text = schema.TextLine(title = u'Text',required = True) 

    steps = schema.Tuple(title = u'Step micro steps', 
                         required = True)

    validation = GlobalObject(title = u'Precondition method.',
                              description = u'Should return true if the step can be visible.',
                              required = False)

    def isVisible(context):
        """ Return true is the step can be visible """

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

