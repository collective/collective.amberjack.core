from zope.interface import Interface
class IRegistrationUtility(Interface):
    pass

class RegistrationUtility:
    
    def __init__(self):
        self.tours = list()
    
    def add(self, tour):
        self.tours.append(tour)
        
    def getTours(self):
        return self.tours


