from collective.amberjack.core.interfaces import IAmberjackSkin
from collective.amberjack.core.interfaces import ITourManager
from zope.component import getUtility
from zope.component import getUtilitiesFor
from zope.interface import implements
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


class AvailableToursVocabulary(object):
    implements(IVocabularyFactory)

    def __call__(self, context):
        manager = getUtility(ITourManager)
        tours = manager.getTours(context)
        terms = [SimpleTerm(value=tour, token=tour_id, title=tour.title)
                 for (tour_id, tour) in tours]
        return SimpleVocabulary(terms)


class AvailableSkinsVocabulary(object):
    implements(IVocabularyFactory)

    def __call__(self, context):
        terms = [SimpleTerm(skin, name, skin.title)
                 for name, skin in getUtilitiesFor(IAmberjackSkin)]
        return SimpleVocabulary(terms)
