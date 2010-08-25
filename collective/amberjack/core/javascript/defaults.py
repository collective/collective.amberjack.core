from Products.Five.browser import BrowserView
from zope.i18n import translate
from zope.i18nmessageid import MessageFactory
from zope.component import getUtility
from zope.app.component.hooks import getSite

from collective.amberjack.core.interfaces import ITour

_ = MessageFactory("collective.amberjack.core")
PMF = MessageFactory('plone')

class AmberjackDefaults(BrowserView): 
    def __call__(self, context, request):
        constants = """
            if (AmberjackPlone){
                AmberjackPlone.aj_plone_consts['Error'] = '%s';
                AmberjackPlone.aj_plone_consts['ErrorValidation'] = '%s';
                AmberjackPlone.aj_plone_consts['BrowseFile'] = '%s';
                
            }
        """ % (PMF(u'Error'),
               PMF(u'Please correct the indicated errors.'),
               _(u'Please select a file.'),
               )
        rootTool = getUtility(ITour, 'collective.amberjack.core.toursroot')
        url = rootTool.getToursRoot(getSite(),context)
        portal_url = self.context.portal_url()
        return """
        function loadDefaults(){
            Amberjack.onCloseClickStay = true;
            Amberjack.doCoverBody = false;
            Amberjack.PORTAL_URL = '%s/';
            Amberjack.BASE_URL = '%s/';
            Amberjack.textOf = "%s";
            
            %s
        }
        """  % (portal_url,
                url, 
                translate(_('separator-between-steps', default=u"of"),context=self.request),
                constants)