import doctest
import unittest
#from zope.app.testing import placelesssetup

from collective.amberjack.core.tests import zcml_template

def test_suite():

    return unittest.TestSuite((
            doctest.DocFileSuite('README.txt',
                         package='collective.amberjack.core',
                         optionflags=(
                             doctest.ELLIPSIS +
                             doctest.NORMALIZE_WHITESPACE +
                             doctest.REPORT_NDIFF),
                         globs = {'template': zcml_template},
#                         setUp=placelesssetup.setUp,
#                         tearDown=placelesssetup.tearDown,
                         ),
            ))
