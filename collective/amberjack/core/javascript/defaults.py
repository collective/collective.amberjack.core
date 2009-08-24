from Products.Five.browser import BrowserView
from zope.i18n import translate
from zope.i18nmessageid import MessageFactory

_ = MessageFactory("collective.amberjack.core")

class AmberjackDefaults(BrowserView): 
    def __call__(self, context, request):
        url = self.context.portal_url()
        return """
        function loadDefaults(){
            Amberjack.onCloseClickStay = true;
            Amberjack.doCoverBody = false;
            Amberjack.BASE_URL = '%s/';
            Amberjack.textOf = "%s";
        }
        """  % (url, translate(_('separator-between-steps', default=u"of"), context=self.request))

