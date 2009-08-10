from Products.Five.browser import BrowserView


class AmberjackDefaults(BrowserView): 
    def __call__(self, context, request):
        url = self.context.portal_url()
        return """
        function loadDefaults(){
            Amberjack.onCloseClickStay = true;
            Amberjack.doCoverBody = false;
            Amberjack.BASE_URL = '%s/';    
        }
        """  % (url, )

