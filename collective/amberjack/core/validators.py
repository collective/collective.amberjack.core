"""Step validators
"""
from Products.CMFCore.utils import getToolByName
from zope.i18nmessageid import MessageFactory
from zope.component import getUtility
from collective.amberjack.core.interfaces import ITour

_ = MessageFactory("collective.amberjack.core")

def isAnonymous(context):
    """Return None if user is anonymous, else an error message."""
    mtool = getToolByName(context, 'portal_membership')
    if not mtool.isAnonymousUser():
        return _(u"You have to be anonymous to execute this step.")

def isAuthenticated(context):
    """Return None if user is authenticated, else an error message."""
    if isAnonymous(context) is None:
        return _(u"You have to be logged in to execute this step.")

def isManager(context, request):
    if not request.AUTHENTICATED_USER.has_role('Manager', context):
        return _(u"You have to be Manager to execute this step.")

def isReviewer(context, request):
    if not request.AUTHENTICATED_USER.has_role('Reviewer', context):
        return _(u"You have to be Reviewer to execute this step.")

def isContributor(context, request):
    if not request.AUTHENTICATED_USER.has_role('Contributor', context):
        return _(u"You have to be Contributor to execute this step.")

def isEditor(context, request):
    if not request.AUTHENTICATED_USER.has_role('Editor', context):
        return _(u"You have to be Editor to execute this step.")

def isReader(context, request):
    if not request.AUTHENTICATED_USER.has_role('Editor', context):
        return _(u"You have to be Reader to execute this step.")

def isFolderCreated(context, path):
    portal = getToolByName(context, 'portal_url').getPortalObject()
    portal_url = portal.absolute_url()
    rootTool = getUtility(ITour, 'collective.amberjack.core.toursroot')
    root = rootTool.getToursRoot(context, context.REQUEST)
    if not portal_url == root:
        relative_url = root.replace(portal_url,'')
        if relative_url.startswith('/'):
             relative_url = relative_url[1:]
        root = portal.unrestrictedTraverse(relative_url.split('/'))
    else:
        root = portal
    
    if path.startswith('/'):
             path = path[1:]    
    myfolder = root.unrestrictedTraverse(str(path).split('/'), None)
    if myfolder is None:
        return _(u"The path [%s] doesn't exist yet. Please close this tour and start the first tour." %root+path) 

def isNotFolderCreated(context, path):
    if isFolderCreated(context, path) is None:
        return _(u"Please remove the [MyFolder] folder to start the tour.")

_validators_ = (
  isNotFolderCreated,
  isFolderCreated,
  isReader,
  isEditor,
  isContributor,
  isReviewer,
  isManager,
  isAuthenticated,
  isAnonymous,
)
