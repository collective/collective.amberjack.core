# -*- coding: utf-8 -*-
from plone.memoize.view import memoize
from Products.Five import BrowserView
from zope.interface import implements, Interface

class ITourView(Interface):
    """
    the Tour interface
    """


class TourView(BrowserView):
    """
    tour view
    """
    implements(ITourView)
        
    def __init__(self, context, request, view, manager): 
        self.context = context 
        self.request = request  
    
    @memoize
    def portal(self):
        return self.context.portal_url()
    
    def javascriptSteps(self):
        """
        {'text': '', 'idStep': 'view_tabular', 'description': 'uno', 'selector': ''}
        """
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