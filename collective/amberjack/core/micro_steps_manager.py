from collective.amberjack.core.interfaces import IMicroStepsDefinition
from collective.amberjack.core.interfaces import IMicroStepsManager
from zope.component import getUtilitiesFor
from zope.interface import implements

class MicroStepsManager(object):
    implements(IMicroStepsManager)

    def getSteps(self, context=None):
        for name, microstep in getUtilitiesFor(IMicroStepsDefinition):
            for stepdef in microstep.stepsdefinition:
                yield stepdef

class MicroStep(object):
    def __init__(self, stepsdefinition):
        self.stepsdefinition = stepsdefinition