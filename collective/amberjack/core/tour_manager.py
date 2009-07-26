from zope.interface import Interface, implements
from zope.component.exceptions import ComponentLookupError
from Products.CMFCore.utils import getToolByName
from zope.component import getMultiAdapter, getUtility, provideUtility, getUtilitiesFor, queryUtility
from collective.amberjack.core.interfaces import ITourDefinition

class IManageTourUtility(Interface):
    
    def add(tour):
        """
            adds a packagedtour to the available tours
        """
        
    def getTours(context):
        """
            given a context, it returns both the packaged and meta tours (tourId, title)
        """

    def getTour(tourId, context, request):
        """
            returns the view that draws the complete tour
        """
        
class ManageTourUtility:
    implements(IManageTourUtility)
    
    def add(self, tour):
        provideUtility(component=tour,   provides=ITourDefinition, name=tour.tour['tourId'])
        
    def getTours(self, context):
        packagedtours = [(name, tour.tour['title']) for name, tour in getUtilitiesFor(ITourDefinition)]
        
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
        from zope.component import provideUtility
        provideUtility(component=ManageTourUtility())
        getUtility(IManageTourUtility).add(tour)