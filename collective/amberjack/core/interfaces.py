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

class IAmberjackSkin(Interface):
    """Register an Amberjack skin.

       The skin resources have to be accessible from the url
       skin/<utility_name>/
       Example:
       http://nohost:8080/plone/skin/<utility_name>/control.tpl.js
    """
    title = schema.TextLine(title=u"The title of the skin shown in the select menu")
