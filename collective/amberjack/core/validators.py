from Products.CMFCore.utils import getToolByName

def isAnonymous(context):
    """ 
    Step validator.
    Return true if user is anonymous.
    """
    mtool = getToolByName(context, 'portal_membership')
    return mtool.isAnonymousUser()

def isAuthenticated(context):
    """
    Step validator.
    Return true if user is authenticated.
    """
    return not isAnonymous(context)

