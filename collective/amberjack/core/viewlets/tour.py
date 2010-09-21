# -*- coding: utf-8 -*-
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets import common

from zope.component import getUtility
from zope.schema.vocabulary import getVocabularyRegistry

from collective.amberjack.core.interfaces import ITour
from collective.amberjack.core.tour_manager import ITourManager
import urllib
import re

class TourViewlet(common.ViewletBase):
    index = ViewPageTemplateFile('tour.pt')

    def update(self):
        super(TourViewlet, self).update()

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
        manager = getUtility(ITourManager)
        return manager.getTour(tourId, self.context)

    def highlight(self, step):
        if (step._options['blueprint']=='collective.amberjack.blueprints.windmillmicrostep'):
            if step.method.find('waits.')!=-1 or step.method=='highlight':
                return u'display:none'

        if step.method != u'':
            return u''
        else:
            return u'display:none'

    def getStepUrl(self, url):
        rootTool = getUtility(ITour, 'collective.amberjack.core.toursroot')
        navigation_root_url = rootTool.getToursRoot(self.context, self.request, url)

        if url.startswith('aj_'):
            return url
        if(url.startswith(navigation_root_url)):
            if(re.search(r'(\d{4})-(\d{2})-(\d{2})',url)!=None): #Use regular expression for check if the url contains a temporary date
                return 'aj_any_url'
            else:
                url=url[url.find(navigation_root_url)+len(navigation_root_url):]
        if url.startswith('ABS'):
            url=url[3:]

        url = urllib.quote(url)

        if url.startswith('/') or url == '':
            url = navigation_root_url + url
        else:
            url = navigation_root_url + '/' + url
        return url

    def _expandSelector(self, selector):
        return selector.replace('AJ_ROOT', self.navigation_root_url)

    def getMacroSteps(self):
        return self.tour.steps

    def getStepNumber(self, step):
        """Add the step to the ajsteps list and return its position"""
        if not step in self.ajsteps:
            self.ajsteps.append(step)
        return self.ajsteps.index(step) + 1


    def javascriptSteps(self):
        """Return an Array:
        [new AjStep('method', 'selector', 'text'), ...]
        """
        try:
            aj = """
            var AjSteps = [
                    """
            cnt = 0
            for step in self.ajsteps:

                if step._options['blueprint']=='collective.amberjack.blueprints.windmillmicrostep':
                    ajstep = """new AjWindmillStep('%s',"%s","%s","%s","%s")""" % (step.method,
                                                                      step.selector.replace('"','\\"'),
                                                                      step.text.replace('\\"','"').replace('"','\\"'), #get the right formatted text from method "editor" without causing error in the others
                                                                      step.required,
                                                                      step.condition.replace('\\"','"').replace('"','\\"')) 
                else:
                    ajstep = """new AjStep('%s','%s',"%s")""" % (step.method,
                                                             self._expandSelector(step.selector),
                                                             step.text.replace('"','\\"'))

                if cnt+1 != len(self.ajsteps):
                    ajstep += """,
                    """
                aj += ajstep
                cnt+=1

            return aj + """
            ]
            """
        except Exception, inst: #XXX put the right Error
            self.context.plone_log(inst)
            return ''

    def _choosenSkin(self):
        try:
            skinId = self.request['skinId']
        except KeyError:
            try:
                skinId = self.request.cookies['ajcookie_skinId']
            except KeyError:
                return None
        return skinId

    def nextTour(self):
        """If a next tour is available, return
        {'url': 'url to run next tour',
         'title': u'next tour url'}
        else None
        """
        rootTool = getUtility(ITour, 'collective.amberjack.core.toursroot')
        navigation_root_url = rootTool.getToursRoot(self.context, self.request)

        tour_id = self.tour.tourId
        vr = getVocabularyRegistry()
        vocab = vr.get(self.context, "collective.amberjack.core.tours")
        previous_term = None
        for term in vocab:
            if previous_term is not None and previous_term.token == tour_id:
                return {'url': '%s?tourId=%s&skinId=%s' % (navigation_root_url, term.token, self._choosenSkin()),
                        'title': term.title}
            previous_term = term
        return None
