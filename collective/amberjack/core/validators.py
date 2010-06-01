"""Step validators
"""
from Products.CMFCore.utils import getToolByName
from zope.i18nmessageid import MessageFactory

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

def isFolderCreated(context, *args):
    portal = getToolByName(context, 'portal_url').getPortalObject()
    myfolder = getattr(portal, 'myfolder', None)
    if myfolder is None:
        return _(u"The [MyFolder] folder doesn't exist yet. Please close this tour and start the first tour.")

def isNotFolderCreated(context, *args):
    if isFolderCreated(context) is None:
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
