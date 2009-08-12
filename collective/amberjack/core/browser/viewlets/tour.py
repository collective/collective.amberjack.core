# -*- coding: utf-8 -*-
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets import common

from zope.component import getUtility
from zope.i18n import translate

from collective.amberjack.core.tour_manager import IManageTourUtility

SSPAN = '<span class="ajHighlight">'
ESPAN = '</span>'


class TourViewlet(common.ViewletBase):
    index = ViewPageTemplateFile('tour.pt')

    def update(self):
        super(TourViewlet, self).update()
        # we have self.site_url
        self.tour = self._choosenTour()
        self.enabled = self.tour is not None
        # self.tour may not be traversable, so we use view/tourId
        # instead of view/tour/tourId in the template
        if self.enabled:
            self.tourId = self.tour.tourId
            self.ajsteps = []
    
    def _choosenTour(self):
        try:
            tourId = self.request['tourId']
        except KeyError:
            try:
                tourId = self.request.cookies['ajcookie_tourId']
            except KeyError:
                return None
        
        manager = getUtility(IManageTourUtility)
        return manager.getTour(tourId, self.context, self.request)

    def _highlight(self, steps):    
        _steps = []
        for step in steps:
            desc = translate(step['description'], context=self.request)
            step['description'] = desc.replace('[', SSPAN).replace(']', ESPAN)
            _steps.append(step)
        return _steps

    def _getMacroStepUrl(self, url):
        if url.startswith('/') or url == '':
            url = self.site_url + url
        else:
            url = self.site_url + '/' + url
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
