from collective.amberjack.core.tour_manager import IManageTourUtility
from zope.component import getUtility
from zope.interface import implements
from zope.schema.vocabulary import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


class AvailableToursVocabulary(object):
    implements(IVocabularyFactory)

    def __call__(self, context):
        context = getattr(context, 'context', context)
        manager = getUtility(IManageTourUtility)
        
        tours = manager.getTours(context)
        
        items = [SimpleTerm(value=tourId, token=title) for (tourId, title) in tours]
        return SimpleVocabulary(items)

AvailableToursVocabularyFactory = AvailableToursVocabulary()
