# -*- coding: utf-8 -*-
from plone.memoize.view import memoize
from Products.Five import BrowserView
from zope.i18n import translate
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

SSPAN = '<span class="ajHighlight">'
ESPAN = '</span>'


class TourView(BrowserView):
    """Tour view"""
    
    __call__ = ViewPageTemplateFile("tour.pt")
    
    def __init__(self, context, request):
        self.tour = context
        self.context = context
        self.request = request
        self.ajsteps = []

    def setContext(self, context):
        # We need to overwrite the context because a Tour oject has not REQUEST attribute...
        self.context = context

    def tourId(self):
        return self.tour.tourId
    
    def _highlight(self, steps):    
        _steps = []
        for step in steps:
            desc = translate(step['description'], context=self.request)
            step['description'] = desc.replace('[', SSPAN).replace(']', ESPAN)
            _steps.append(step)
        return _steps

    @memoize
    def portal(self):
        return self.context.portal_url()

    def _getMacroStepUrl(self, url):
        if url.startswith('/') or url == '':
            url = self.portal() + url
        else:
            url = self.portal() + '/' + url
        return url

    def getMacroSteps(self):
        results = []
        for macrostep in self.tour.steps():
            _macrostep = {}
            for key, value in macrostep.items():
                if key == 'steps':
                    _macrostep[key] = self._highlight(tuple(macrostep['steps']))
                elif key == 'url':
                    _macrostep[key] = self._getMacroStepUrl(value)
                else:
                    _macrostep[key] = value
            results.append(_macrostep)
        return results

    def getStepNumber(self, step):
        """Add the step to the ajsteps list and return its position"""
        if not step in self.ajsteps:
            self.ajsteps.append(step)
        return self.ajsteps.index(step) + 1
    
    def javascriptSteps(self):
        """Return a dict:
        {'1': new AjStep('idStep': 'selector', 'text'), ...}
        """
        try:
            aj = """
            var AjSteps = {
                    """
            for idx, step in enumerate(self.ajsteps):
                ajstep = """'%s': new AjStep('%s','%s','%s')""" % (idx + 1, step['idStep'], step['selector'], step['text'])
                if idx + 1 != len(self.ajsteps):
                    ajstep += """,
                    """
                aj += ajstep
            
            return aj + """
            }
            """
        except: #XXX put the right Error
            return ''
