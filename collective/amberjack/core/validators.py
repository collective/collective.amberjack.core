"""Step validators
"""
from Products.CMFCore.utils import getToolByName
from zope.i18nmessageid import MessageFactory

_ = MessageFactory("collective.amberjack.core")

def isAnonymous(context):
    """Return True if user is anonymous."""
    mtool = getToolByName(context, 'portal_membership')
    if not mtool.isAnonymousUser():
        return _(u"You have to be anonymous to start this tour.")

def isAuthenticated(context):
    """Return True if user is authenticated."""
    if isAnonymous(context) is None:
        return _(u"You have to be logged in to start this tour.")

