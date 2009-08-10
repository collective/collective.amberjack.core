# -*- coding: utf-8 -*-
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets import common
from zope.component import getUtility
from collective.amberjack.core.tour_manager import IManageTourUtility


class TourViewlet(common.ViewletBase):
    index = ViewPageTemplateFile('tour.pt')
    
    def site(self):
        return self.context.portal_url()
    
    def choosenTour(self):
        try:
            try:
                tourId = self.request['tourId']
            except KeyError:
                tourId = self.request.cookies['ajcookie_tourId']
            
            manager = getUtility(IManageTourUtility)
            return manager.getTour(tourId, self.context, self.request)
        
        except KeyError:
            return ''
