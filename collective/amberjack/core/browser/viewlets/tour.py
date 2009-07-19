# -*- coding: utf-8 -*-
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets import common
from Products.CMFCore.utils import getToolByName
from zope.component import getMultiAdapter

class TourViewlet(common.ViewletBase):
    """Viewlet for the demo"""
    
    render = ViewPageTemplateFile('tour.pt')
    
    def __init__(self, context, request, view, manager): 
        self.context = context 
        self.request = request
        
        
    def site(self):
        return self.context.portal_url()
    
    def choosenTour(self):
        try:
            try:
                tourId = self.request['tourId']
            except KeyError:
                tourId = self.request.cookies['ajcookie_tourId']
            portal_catalog = getToolByName(self.context, 'portal_catalog', None)
            #actually I just search in portal_catalog
            tour = portal_catalog(portal_type='ajtour', getTourId=tourId)
            try:
                view = getMultiAdapter((tour[0].getObject(), self.request), name='tour')
                return view()
            except IndexError:
                return ''
        except KeyError:
            return ''