"""Step validators
"""
from Products.CMFCore.utils import getToolByName
from zope.i18n import translate
from zope.i18nmessageid import MessageFactory
from zope.component import getUtility
from collective.amberjack.core.interfaces import ITour

_ = MessageFactory("collective.amberjack.core")
_plone = MessageFactory("plone")


class AmberjackException(Exception):
    pass


def isAnonymous(context):
    """Return None if user is anonymous, else an error message.
    """
    mtool = getToolByName(context, 'portal_membership')
    if not mtool.isAnonymousUser():
        raise AmberjackException(
                _(u"You have to be anonymous to execute this step."))
    return None


def isAuthenticated(context):
    """Return None if user is authenticated, else an error message.
    """
    if isAnonymous(context) is None:
        raise AmberjackException(
                _(u"You have to be logged in to execute this step."))
    return None


def hasRole(context, request, role):
    if request.AUTHENTICATED_USER.has_role('Manager', context):
        return None
    if not request.AUTHENTICATED_USER.has_role(role, context):
        raise AmberjackException(translate(
                _(u"You have to be ${role} to execute this step.",
                  mapping={'role': _plone(role)})))
    return None


def isCreated(context, path):
    portal = getToolByName(context, 'portal_url').getPortalObject()
    portal_url = portal.absolute_url()
    rootTool = getUtility(ITour, 'collective.amberjack.core.toursroot')
    root = rootTool.getToursRoot(context, context.REQUEST)
    if not portal_url == root:
        relative_url = root.replace(portal_url, '')
        if relative_url.startswith('/'):
            relative_url = relative_url[1:]
        root = portal.unrestrictedTraverse(relative_url.split('/'))
    else:
        root = portal
    if path.startswith('/'):
        path = path[1:]
    myfolder = root.aq_base.unrestrictedTraverse(str(path).split('/'), None)
    if myfolder is None:
        raise AmberjackException(translate(
                _(u"The object [${path}] doesn't exist yet.",
                  mapping={'path': path}), target_language=portal.Language()))
    return None


def isNotCreated(context, path):
    try:
        isCreated(context, path)
    except AmberjackException:
        return None
    portal = getToolByName(context, 'portal_url').getPortalObject()
    raise AmberjackException(translate(
            _(u"Please remove the [${path}] object to start the tour.",
              mapping={'path': path}), target_language=portal.Language()))


_validators_ = (
  isNotCreated,
  isCreated,
  hasRole,
  isAuthenticated,
  isAnonymous,
)
