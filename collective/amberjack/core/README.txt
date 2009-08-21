Meta directive registration
===========================

collective.amberjack.core provides useful tour registration using zcml approach. 
First we need to include meta.zcml in our package::
	
	>>> from Products.Five import zcml
	>>> import collective.amberjack.core
	>>> zcml.load_config('meta.zcml', collective.amberjack.core)
		
Than registration is as simple as::

    >>> simple_directive = '''
    ... <collective.amberjack:tour
    ...     tourdescriptor="collective.amberjack.core.tests.base.DummyTour"
    ... />'''
    >>> config_zcml = template % simple_directive
    >>> zcml.load_string(config_zcml) 

Let's check the TourDefinition utility to see our dummy tour::

	>>> from collective.amberjack.core.interfaces import ITourDefinition
	>>> from zope.component import getUtility
	>>> utility = getUtility(ITourDefinition, name='dummy_id')
	>>> utility.tour['title']
	u'Dummy title'

