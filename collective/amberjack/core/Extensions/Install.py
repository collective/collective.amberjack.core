# -*- coding: utf-8 -*-

from cStringIO import StringIO

from zope.component import getSiteManager

from Products.CMFCore.utils import getToolByName
from collective.amberjack.core.interfaces import IAjConfiguration


def uninstall(self, reinstall=False, out=None):
    if out is None:
        out = StringIO()

    getSiteManager(self).unregisterUtility(self['portal_amberjack'],
                                           IAjConfiguration)
    # uninstall configlets
    try:
        cptool = getToolByName(self, 'portal_controlpanel')
        cptool.unregisterConfiglet('collective.amberjack')
        out.write('Removing collective.amberjack Configlet')
    except:
        out.write('Failed to remove collective.amberjack Configlet')

    return out.getvalue()
