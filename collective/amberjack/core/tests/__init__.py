zcml_template = '''
<configure
    xmlns="http://namespaces.zope.org/zope"
    xmlns:collective.amberjack="http://namespaces.plone.org/collective.amberjack.core">
    
    %s
    
</configure>'''

DummyTour = {'tourId': 'dummy_id',
             'title': u'Dummy title',
             'steps': ()
             }