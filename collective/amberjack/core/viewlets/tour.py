# -*- coding: utf-8 -*-
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets import common

from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.i18n import translate
from zope.schema.vocabulary import getVocabularyRegistry

from collective.amberjack.core.tour_manager import IManageTourUtility
from collective.amberjack.core.tour import Step
import urllib

SSPAN = '<span class="ajHighlight">'
ESPAN = '</span>'


class TourViewlet(common.ViewletBase):
    index = ViewPageTemplateFile('tour.pt')

    def update(self):
        # super(TourViewlet, self).update()
        # self.navigation_root_url exist only in plone.app.layout > 1.1.8
        # so we create here to be compatible with Plone 3.2.3
        self.portal_state = getMultiAdapter((self.context, self.request),
                                            name=u'plone_portal_state')
        self.navigation_root_url = unicode(self.portal_state.navigation_root_url())

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
        if not tourId:
            return None
        manager = getUtility(IManageTourUtility)
        return manager.getTour(tourId, self.context)

    def _highlight(self, steps):    
        _steps = ()
        for step in steps:
            desc = translate(step['description'], context=self.request)
            step['description'] = desc.replace('[', SSPAN).replace(']', ESPAN)
            if (step['idStep'] != u''):
                step['display'] = u''
            else:
                step['display'] = u'display:none'
                
            _steps += (step,)
        return _steps

    def _getMacroStepUrl(self, url):
        url = urllib.quote(url)
        if url.startswith('/') or url == '':
            url = self.navigation_root_url + url
        else:
            url = self.navigation_root_url + '/' + url
        return url

    def getMacroSteps(self):
        results = []        
        for macrostep in self.tour.steps:
            _macrostep = {}
            for key, value in macrostep.items():
                if key == 'steps':
                    _macrostep[key] = self._highlight(tuple(macrostep['steps']))
                elif key == 'url':
                    _macrostep[key] = self._getMacroStepUrl(value)
                else:
                    _macrostep[key] = value
            results.append(Step(**_macrostep))
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

    def nextTour(self):
        """If a next tour is available, return
        {'url': 'url to run next tour',
         'title': u'next tour url'}
        else None
        """
        tour_id = self.tour.tourId
        vr = getVocabularyRegistry()
        vocab = vr.get(self.context, "collective.amberjack.core.tours")
        previousTerm = None
        for term in vocab:
            if previousTerm is not None and previousTerm.token == tour_id:
                return {'url': '%s?tourId=%s' % (self.navigation_root_url, term.token),
                        'title': term.title}
            previousTerm = term
        return None





