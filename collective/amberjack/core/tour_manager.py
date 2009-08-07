from collective.amberjack.core.interfaces import ITourDefinition
from Products.CMFCore.utils import getToolByName
from zope.component import getMultiAdapter, getUtility, provideUtility, getUtilitiesFor, queryUtility
from zope.component.exceptions import ComponentLookupError
from zope.interface import Interface, implements


class IManageTourUtility(Interface):
    
    def add(tour):
        """Add a packagedtour to the available tours."""
        
    def getTours(context):
        """Given a context, return both the packaged
        and meta tours (tourId, title)."""

    def getTour(tourId, context, request):
        """Return the view that draws the complete tour."""
        
class ManageTourUtility(object):
    implements(IManageTourUtility)
    
    def add(self, tour):
        provideUtility(component=tour, provides=ITourDefinition,
            name=tour.tour['tourId'])
        
    def getTours(self, context):
        packagedtours = [(name, tour.tour['title'])
            for name, tour in getUtilitiesFor(ITourDefinition)]
        
        portal_catalog = getToolByName(context, 'portal_catalog', None)
        tours = portal_catalog(portal_type='ajtour')
        metatours = [(b.getTourId, b.Title) for b in tours]
        
        return sorted(packagedtours + metatours)

    def getTour(self, tourId, context, request):
        try:
            tour = queryUtility(ITourDefinition, name=tourId)
            if tour:
                try:                    
                    view = getMultiAdapter((tour, request), name='tour')
                    view.setContext(context)
                    return view()
                except IndexError:
                    return '' 
            else:
                portal_catalog = getToolByName(context, 'portal_catalog', None)
                tour = portal_catalog(portal_type='ajtour', getTourId=tourId)
                try:
                    view = getMultiAdapter((tour[0].getObject(), request), name='tour')
                    return view()
                except IndexError:
                    return ''
            
        except KeyError:
            return ''
        
def registerTour(tour):
    try:
        getUtility(IManageTourUtility).add(tour)
    except ComponentLookupError:
        provideUtility(component=ManageTourUtility())
        getUtility(IManageTourUtility).add(tour)
