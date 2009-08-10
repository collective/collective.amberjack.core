# -*- coding: utf-8 -*-
from plone.memoize.view import memoize
from Products.Five import BrowserView
from zope.interface import implements, Interface
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class ITourView(Interface):
    """The Tour interface."""
    
    def tourId():
        pass
    
    def steps():
        pass
    
    def _highlight(steps):
        pass
    
    def getStepNumber(step):
        pass
    
    def getSteps(item):
        pass
    
    def portal_catalog():
        pass
    
    def portal():
        pass
    
    def javascriptSteps():
        pass

class TourView(BrowserView):
    """Tour view"""
    implements(ITourView)
    
    __call__ = ViewPageTemplateFile("tour.pt")
    
    def __init__(self, context, request):
        self.context = context 
        self.request = request
        self.ajsteps = list()
    
    def tourId(self):
        raise NotImplementedError("you shouldn't use this directly: subclass it")
    
    def steps(self):
        raise NotImplementedError("you shouldn't use this directly: subclass it")
    
    def getSteps(self, item):
        raise NotImplementedError("you shouldn't use this directly: subclass it")
    
    def _highlight(self, steps):    
        sspan = '<span class="ajHighlight">'
        espan = '</span>'
        _steps = list()
        for step in steps:
            step['description'] = step['description'].replace('[', sspan).replace(']', espan)
            _steps.append(step)
        return _steps
    
    def getStepNumber(self, step):
        """Add the step to the ajsteps tuple and return its position"""
        if not step in self.ajsteps:
            self.ajsteps.append(step)
        return self.ajsteps.index(step) + 1
    
    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')
    
    @memoize
    def portal(self):
        return self.context.portal_url()
    
    def javascriptSteps(self):
        """Return a dict:
        {'text': '', 'idStep': 'view_tabular', 'description': 'uno', 'selector': ''}
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
        
        
class PackagedTourView(TourView):    
    def setContext(self, context):
        self.context = context
        
    def tourId(self):
        return self.tour['tourId']
        
    def steps(self):
        """Return a dict:
        {
        url: ..., 
        title: ..., 
        text: ..., 
        steps: ((description, idstep, selector, text), ...)}
        """
        output = list()
        for item in self.tour['ajsteps']:
            url = item['url']
            if url.startswith('/') or url=='':
                url = self.portal() + url
            else:
                url = self.portal() + '/' + url
            d = {
                'url':  url,
                'title': item['title'],
                'text': item['text'],
                'steps': self._highlight(self.getSteps(item)),
                'xpath': item['xpath'],
                'xcontent': item['xcontent'],
                }
            output.append(d)

        return output
            
    def getSteps(self, item):
        return tuple(item['steps'])
