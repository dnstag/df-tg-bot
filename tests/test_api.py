# 
# test/test_api.py - This file is part of DF-TG-Bot
#
# Copyright (c) 2025 Yannick Seibert. All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import unittest
from unittest.mock import patch, MagicMock
from programs.pota.api import POTAAPI

class TestPOTAAPI(unittest.TestCase):

    @patch('programs.pota.api.requests.get')
    def test_get_park(self):
        # Simulierter Rückgabewert für die API
        fake_park = {"reference": "DL-1234", "name": "Black Forest"}

        # Mock-Objekt der API
        mock_api = MagicMock()
        mock_api.get_park.return_value = fake_park

        api = POTAAPI()
        result = api.get_park("DE-0693")

        self.assertEqual(result.name, "DE-0693")
        self.assertEqual(result.description, "Biosphäre Bluesgau")
        self.assertEqual(result.active, True)
        mock_api.get_park.assert_called_once_with("DE-0693")

if __name__ == '__main__':
    unittest.main()