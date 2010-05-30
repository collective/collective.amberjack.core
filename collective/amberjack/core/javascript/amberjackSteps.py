from Products.Five.browser import BrowserView
from zope.component import getUtility
from collective.amberjack.core.interfaces import IMicroStepsManager

class AmberjackSteps(BrowserView):
    """Generate a Javascript structure like this:
    
    AjStandardSteps = {
        selectorKind: selector,
        ...
    }
    
    Differents selectorKind value use in different way the given (optional) selector.    
    """
    def __call__(self, context, request):
        microstepsmanager = getUtility(IMicroStepsManager)
        js = 'AjStandardSteps = {'
        for (key, value) in microstepsmanager.getSteps():
            js += "'%s':'%s',\n" % (key, value)
        
        js += '}'
        return js

