from Products.Five.browser import BrowserView

class AmberjackDefaults(BrowserView): 
    def __init__(self, context, request): 
        self.context = context 
        self.request = request
        
    def __call__(self, context, request):
        url = self.context.portal_url()
        return """
        function loadDefaults(){
            Amberjack.onCloseClickStay = true;
            Amberjack.doCoverBody = false;
            Amberjack.BASE_URL = '%s/';    
        }
        """  % (url, )
