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

class IFileArchiveTourRegistration(Interface):
    """ """
    zipfile = schema.Bytes(
        title=u'Choose archive file',
        required=False)

class IWebTourRegistration(Interface):
    """ """
    url = schema.URI(
        title=u'Choose url',
        required=False)

class ITourRegistrationForm(IFileArchiveTourRegistration,
                            IWebTourRegistration):
    """ """

