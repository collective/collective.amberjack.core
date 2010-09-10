from collective.amberjack.core.interfaces import ITourRegistration, \
    IControlPanelTourRegistration, IAjConfiguration, IAmberjackSetupForm
from plone.app.controlpanel.form import ControlPanelForm
from plone.fieldsets.fieldsets import FormFieldsets
from zope.component import adapts
from zope.interface import implements
from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from Products.CMFPlone.interfaces import IPloneSiteRoot
from zope.component import queryUtility

class AJControlPanelAdapter(SchemaAdapterBase):
    adapts(IPloneSiteRoot)
    implements(IAmberjackSetupForm)
    zipfile = None
    url = None
        
    def get_sandbox(self):
        return self.context.portal_amberjack.sandbox

    def set_sandbox(self, value):
        setattr(self.context.portal_amberjack,'sandbox',value)

    sandbox = property(get_sandbox, set_sandbox)

class AJControlPanelForm(ControlPanelForm):

    tour_registration = FormFieldsets(IControlPanelTourRegistration)
    tour_registration.label = u'Tour registration'
    tour_registration.id = 'tour_registration'

    configuration = FormFieldsets(IAjConfiguration)
    configuration.label = u'Configuration'
    configuration.id = 'configuration'

    form_fields = FormFieldsets(configuration, tour_registration)

    label = u"Amberjack Setup"
    description = u"Configuraion for Amberjack."
    form_name = u"Amberjack Setup"

    def _on_save(self, data=None):
        for name,source in data.items():
            if not source:
                continue
            reg = queryUtility(ITourRegistration, name)
            if not reg:
                continue
            registration = reg(source, request=self.context.REQUEST)
            registration.register()
