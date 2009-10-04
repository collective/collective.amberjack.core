from Products.Five.browser import BrowserView
from zope.component import getUtility
from collective.amberjack.core.interfaces import IMicroStepsManager

class AmberjackSteps(BrowserView):
    def __call__(self, context, request):
        amberjackSteps = getUtility(IMicroStepsManager)
        js = 'AjStandardSteps = {'
        for (key, value) in amberjackSteps.getSteps():
            js += "'%s':'%s',\n" % (key, value)
        
        js += '}'
        return js

