from collective.amberjack.core.interfaces import ITourDefinition
from Products.CMFCore.utils import getToolByName
from zope.component import getMultiAdapter, getUtility, provideUtility, getUtilitiesFor, queryUtility
from zope.component.interfaces import ComponentLookupError
from zope.interface import Interface, implements


class IManageTourUtility(Interface):
    
    def add(tour):
        """Add a packagedtour to the available tours."""
        
    def getTours(context):
        """Given a context, return both the packaged
        and meta tours (tourId, title)."""

    def getTour(tourId, context, request):
        """Return the tour with the given tourId (object implementing ITourDefinition), None if not found."""
        
class ManageTourUtility(object):
    implements(IManageTourUtility)
    
    def add(self, tour):
        provideUtility(component=tour, provides=ITourDefinition,
            name=tour.tourId())
        
    def getTours(self, context):
        packagedtours = [(name, tour.title())
            for name, tour in getUtilitiesFor(ITourDefinition)]
        
        portal_catalog = getToolByName(context, 'portal_catalog', None)
        tours = portal_catalog(portal_type='ajtour')
        metatours = [(b.getTourId, b.Title) for b in tours]
        
        return sorted(packagedtours + metatours)

    def getTour(self, tourId, context, request):
        tour = queryUtility(ITourDefinition, name=tourId)
        if tour is not None:
            return tour
        else:
            portal_catalog = getToolByName(context, 'portal_catalog', None)
            brains = portal_catalog(portal_type='ajtour', getTourId=tourId)
            if brains:
                return ITourDefinition(brains[0].getObject())
            else:
                return None
        
def registerTour(tour):
    try:
        getUtility(IManageTourUtility).add(tour)
    except ComponentLookupError:
        provideUtility(component=ManageTourUtility())
        getUtility(IManageTourUtility).add(tour)
