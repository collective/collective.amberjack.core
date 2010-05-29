from collective.amberjack.core.experimental.interfaces import ITourRegistration
from plone.app.controlpanel.form import ControlPanelForm
from zope.component import adapts
from zope.formlib import form
from zope.interface import implements
from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from Products.CMFPlone.interfaces import IPloneSiteRoot
from zope.component import getUtility

class AJControlPanelAdapter(SchemaAdapterBase):
    adapts(IPloneSiteRoot)
    implements(ITourRegistration)

    def set_uri(self, value):
        reg = getUtility(ITourRegistration, 'zip_archive')
        registration = reg(value)
        registration.register()

    def get_uri(self):
        return None

    uri = property(get_uri, set_uri)

class AJControlPanelForm(ControlPanelForm):
    form_fields = form.FormFields(ITourRegistration)
    label = u"Amberjack tour registration"
    description = u"Registration of the tours."
    form_name = u"Tours registraion"
