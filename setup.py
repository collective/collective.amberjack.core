from setuptools import setup, find_packages
import os

version = '1.0dev'

setup(name='collective.amberjack.core',
      version=version,
      description="The Amberjack layer",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='Massimo Azzolini',
      author_email='massimo@redturtle.net',
      url='https://svn.plone.org/svn/collective/collective.amberjack.core',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective', 'collective.amberjack'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'plone.app.layout',
          'Products.CMFCore',
          'Products.Five',
          'Products.GenericSetup',
          'zope.component',
          'zope.configuration',
          'zope.i18n',
          'zope.interface',
          'zope.schema',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
