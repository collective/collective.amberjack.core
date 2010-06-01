from zope.interface import implements
from plone.i18n.normalizer.interfaces import IIDNormalizer
from zope.component import getUtility
from collective.amberjack.core.interfaces import ITour
from collective.amberjack.core import utils

import UserDict
import os

class Tour(UserDict.DictMixin):
    implements(ITour)

    def __init__(self, configuration, tour_id):
        try:
            self._filename = os.path.basename(configuration.name)
        except AttributeError:
            self._filename = 'no_filename'
        self._raw = utils._load_config(configuration)
        self._data = {}
        self._options = self._raw['amberjack']
        self._steps_ids = self._options['steps'].splitlines()
        self.steps = utils.constructTour(self, self._steps_ids)
        self.title = self._options['title']
        self.setTourId(tour_id)

    def setTourId(self, tour_id):
        normalizer = getUtility(IIDNormalizer)
        self.tourId = normalizer.normalize('%s.%s' % (tour_id, self.title))

    def __getitem__(self, step):
        try:
            return self._data[step]
        except KeyError:
            pass
        data = self._raw[step]
        options = utils.Options(self, step, data)
        self._data[step] = options
        options._substitute()
        return options

    def __setitem__(self, key, value):
        raise NotImplementedError('__setitem__')

    def __delitem__(self, key):
        raise NotImplementedError('__delitem__')

    def keys(self):
        return self._raw.keys()

    def __repr__(self):
        return ('<AmberjackTour based on %s>' % self._filename)
