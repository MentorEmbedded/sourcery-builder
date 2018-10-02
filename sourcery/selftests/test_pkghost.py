# Test sourcery.pkghost.

# Copyright 2018 Mentor Graphics Corporation.

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation; either version 2.1 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, see
# <https://www.gnu.org/licenses/>.

"""Test sourcery.pkghost."""

import unittest

from sourcery.buildcfg import BuildCfg
import sourcery.context
from sourcery.pkghost import PkgHost

__all__ = ['PkgHostTestCase']


class PkgHostTestCase(unittest.TestCase):

    """Test the PkgHost class."""

    def setUp(self):
        """Set up a PkgHost test."""
        self.context = sourcery.context.ScriptContext()

    def test_init(self):
        """Test __init__."""
        host = PkgHost(self.context, 'aarch64-linux-gnu')
        self.assertIs(host.context, self.context)
        self.assertEqual(host.name, 'aarch64-linux-gnu')
        self.assertIsInstance(host.build_cfg, BuildCfg)
        self.assertIs(host.build_cfg.context, self.context)
        self.assertEqual(host.build_cfg.triplet, 'aarch64-linux-gnu')
        cfg = BuildCfg(self.context, 'powerpc-linux-gnu')
        host = PkgHost(self.context, 'powerpc-linux-gnu-hard', cfg)
        self.assertIs(host.context, self.context)
        self.assertEqual(host.name, 'powerpc-linux-gnu-hard')
        self.assertIs(host.build_cfg, cfg)
