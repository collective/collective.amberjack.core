from zope.interface import classProvides, implements
from zope.component import getUtility
from collective.amberjack.core.experimental.interfaces import IStep, IStepBlueprint

SSPAN = '<span class="ajHighlight">'
ESPAN = '</span>'

class Step(object):
    classProvides(IStepBlueprint)
    implements(IStep)
    
    def __init__(self, tour, name, options):
        self._tour = tour
        self._options = options        
        self.microsteps = self.constructMicroSteps(options)
        self.xpath = self._options.get('xpath','')
        self.xcontent = self._options.get('xcontent','')
        self.url = self._options['url']
        self.title = self._options['title']
        self.text = normalizeHTML(self._options.get('text',''))

    def constructMicroSteps(self, options):
        microsteps = options.get('steps','').splitlines()
        results = []
        for microstep_id in microsteps:
            microstep_id = microstep_id.strip()
            if not microstep_id:
                continue
            microstep_options = self._tour[microstep_id]
            blueprint_id = microstep_options['blueprint'].decode('ascii')
            blueprint = getUtility(IStepBlueprint, blueprint_id)
            microstep = blueprint(self._tour, microstep_id, microstep_options)
            if not IStep.providedBy(microstep):
                raise ValueError('Blueprint %s for section %s did not return '
                                 'an IStep' % (blueprint_id, microstep_id))
            results.append(microstep)
        return results

    def validate(self, context, request):
        #ToBeImplemented
        return []

class MicroStep(object):
    classProvides(IStepBlueprint)
    implements(IStep)
    
    def __init__(self, tour, name, options):
        self._tour = tour
        self._options = options
        self.description = normalizeHTML(self._options['description'])
        self.selector = self._options.get('selector','')
        self.text = normalizeHTML(self._options.get('text',''))
        self.idStep = self._options.get('idstep','')
        
def normalizeHTML(text):
    return text.replace('[', SSPAN).replace(']', ESPAN)
