from collective.amberjack.core.interfaces import IAmberjackSkin
from zope.interface import implements


class SafariSkin(object):
    implements(IAmberjackSkin)
    title = u"Safari"

class ModelTSkin(object):
    implements(IAmberjackSkin)
    title = "Model_t"
