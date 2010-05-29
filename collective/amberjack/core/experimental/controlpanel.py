from collective.amberjack.core.experimental.interfaces import ITourRegistration, IFileArchiveTourRegistration, IWebTourRegistration, ITourRegistrationForm
from plone.app.controlpanel.form import ControlPanelForm
from plone.fieldsets.fieldsets import FormFieldsets
from zope.component import adapts
from zope.interface import implements
from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from Products.CMFPlone.interfaces import IPloneSiteRoot
from zope.component import queryUtility

class AJControlPanelAdapter(SchemaAdapterBase):
    adapts(IPloneSiteRoot)
    implements(ITourRegistrationForm)
    zipfile = None
    url = None

class AJControlPanelForm(ControlPanelForm):

    archive = FormFieldsets(IFileArchiveTourRegistration)
    archive.label = u'Archives'
    archive.id = 'archives'

    web = FormFieldsets(IWebTourRegistration)
    web.label = u'Web'
    web.id = 'web'

    form_fields = FormFieldsets(archive, web)

    label = u"Amberjack tour registration"
    description = u"Registration of the tours."
    form_name = u"Tours registraion"

    def _on_save(self, data=None):
        for name,source in data.items():
            if not source:
                continue
            reg = queryUtility(ITourRegistration, name)
            if not reg:
                continue
            registration = reg(source, self.context.REQUEST)
            registration.register()
