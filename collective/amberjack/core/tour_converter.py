"""
migrates a dictionary-based tour into a configuration-based one
./bin/instance run src/collective.amberjack.core/collective/amberjack/core/tour_converter.py <tourId>

tourId is the one specified in the tour definition. e.g.
ajTour = {'tourId': u'basic01_add_and_publish_a_folder',
          'title': ...,
          'steps': ...
                   }

"""
import sys
from zope.component import getUtility
from collective.amberjack.core.tour_manager import ITourManager
from plone.i18n.normalizer.interfaces import IIDNormalizer
from zope.component import getUtility
import ConfigParser

def normalize(noun):
    normalizer = getUtility(IIDNormalizer)
    return normalizer.normalize(noun)

class Converter:

    def __init__(self, tourId, context):
        self.tourId = tourId
        self.context = context
        self.config = ConfigParser.RawConfigParser()
        manager = getUtility(ITourManager)
        self.tour = manager.getTour(tourId, context)

    def convert(self):
        if not self.tour:
            return
        self.config.add_section('amberjack')
        self.config.set('amberjack', 'title', self.tour.__dict__['title'])

        section_steps = ['']
        for step_no, step in enumerate(self.tour.__dict__['steps']):
            step_name = normalize(step['title'])
            section_steps.append(step_name)
            self.convert_step(step, step_no)

        self.set('amberjack', 'steps', section_steps)
        with open('%s.cfg' % self.tourId, 'wb') as configfile:
            self.config.write(configfile)

    def convert_step(self, step, step_no):
        step_name = normalize(step['title'])
        self.config.add_section(step_name)
        self.config.set(step_name, 'blueprint', 'collective.amberjack.blueprints.step')
        for k, v in step.items(): 
            if k == 'validators':
                validators = ['']
                for validator in v:
                    validators.append("'%s'" % validator.__name__)
                self.set(step_name, 'validators', validators)
                continue
            if k == 'steps':
                section_microsteps = ['']
                for i, microstep in enumerate(v):
                    microstep_name = 'microstep_%s_%s' % (step_no, i)
                    self.convert_microstep(microstep, microstep_name)
                    section_microsteps.append(microstep_name)
                if section_microsteps != ['']:
                    self.set(step_name, 'steps', section_microsteps)
                continue

            self.set(step_name, k, v)

    def convert_microstep(self, microstep, microstep_name):
        self.config.add_section(microstep_name)
        self.config.set(microstep_name, 'blueprint', 'collective.amberjack.blueprints.microstep')
        for k, v in microstep.items():
            self.set(microstep_name, k, v)

    def set(self, section, k, v):
        if hasattr(v, '__iter__'):
            if ''.join(v).strip():
                self.config.set(section, k, '\n'.join(v))
        elif v.strip():
           self.config.set(section, k, "'%s'" % v)

def main(app=None):
    tourId = sys.argv[1]
    Converter(tourId, app).convert()

if __name__ == '__main__':
    main(app=app) 

