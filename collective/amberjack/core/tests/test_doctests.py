import doctest
import unittest
from zope.component import testing

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
                         setUp=testing.setUp,
                         tearDown=testing.tearDown,
                         ),
            ))
