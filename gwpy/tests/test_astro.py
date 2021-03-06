# -*- coding: utf-8 -*-
# Copyright (C) Duncan Macleod (2013)
#
# This file is part of GWpy.
#
# GWpy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# GWpy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with GWpy.  If not, see <http://www.gnu.org/licenses/>.

"""Unit test for astro module
"""

import os
import os.path
import tempfile

from compat import unittest

from astropy import units

from gwpy import astro
from gwpy.timeseries import TimeSeries

__author__ = 'Duncan Macleod <duncan.macleod@ligo.org>'


class AstroTests(unittest.TestCase):
    """`TestCase` for the astro module
    """
    framefile = os.path.join(os.path.split(__file__)[0], 'data',
                             'HLV-GW100916-968654552-1.hdf')
    tmpfile = '%s.%%s' % tempfile.mktemp(prefix='gwpy_test_')

    def setUp(self):
        # read data
        self.data = TimeSeries.read(self.framefile, 'L1:LDAS-STRAIN')
        # calculate PSD
        self.psd = self.data.psd(0.4, 0.2, window=('kaiser', 24))

    def test_inspiral_range(self):
        r = astro.inspiral_range(self.psd, fmin=40)
        self.assertEqual(r.unit, units.Mpc)
        self.assertAlmostEqual(r.value, 19.63704209223392)
        return r

    def test_inspiral_range_psd(self):
        r = astro.inspiral_range_psd(self.psd)
        self.assertEqual(r.unit, units.Mpc ** 2 / units.Hertz)
        self.assertAlmostEqual(r.max().value, 7.915847068684727)
        return r

    def test_burst_range(self):
        r = astro.burst_range(self.psd[self.psd.frequencies.value < 1000])
        self.assertEqual(r.unit, units.Mpc)
        self.assertAlmostEqual(r.value, 13.813232309724613)
        return r

    def test_burst_range_spectrum(self):
        r = astro.burst_range_spectrum(
            self.psd[self.psd.frequencies.value < 1000])
        self.assertEqual(r.unit, units.Mpc)
        self.assertAlmostEqual(r.max().value, 35.19303454822539)
        return r


if __name__ == '__main__':
    unittest.main()
