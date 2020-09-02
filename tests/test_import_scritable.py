import gsassier

import unittest


class TestAnacondaImport(unittest.TestCase):
    def test_anaconda_import(self):
        from gsassier import GSASIIscriptable
        self.assertIn('G2Project', dir(GSASIIscriptable))
