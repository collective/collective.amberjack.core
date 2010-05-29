from zope.interface import Interface
from zope import schema

class ITour(Interface):
    """ """

class IStep(Interface):
    """ """

class IStepBlueprint(Interface):
    """ """

class ITourRegistration(Interface):
    """ """
    uri = schema.TextLine(title= u"URI", required=True)
