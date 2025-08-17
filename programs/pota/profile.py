#
# profile.py - This file is part of DF-TG-Bot
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

from programs.profile import Profile
from programs.pota.park import Park
from dataclasses import dataclass

@dataclass
class POTAProfile(Profile):
    """
    Represents a POTA user profile with a callsign and a list of POTA references.
    Inherits from the Profile class.
    """
    activator_sucessful_parks: int = 0
    activator_sucessful_activations: int = 0
    activator_sucessful_qsos: int = 0
    activator_attempted_parks: int = 0
    activator_attempted_activations: int = 0
    activator_attempted_qsos: int = 0
    hunter_parks: int = 0
    hunter_qsos: int = 0

    def __str__(self):
        return super().__str__() + (f", "
                f"activator_sucessful_parks={self.activator_sucessful_parks}, "
                f"activator_sucessful_activations={self.activator_sucessful_activations}, "
                f"activator_sucessful_qsos={self.activator_sucessful_qsos}, "
                f"activator_attempted_parks={self.activator_attempted_parks}, "
                f"activator_attempted_activations={self.activator_attempted_activations}, "
                f"activator_attempted_qsos={self.activator_attempted_qsos}, "
                f"hunter_parks={self.hunter_parks}, "
                f"hunter_qsos={self.hunter_qsos})")
    
    def to_dict(self):
        """
        Converts the POTA profile to a dictionary format.
        """
        return super().to_dict() + {
            "activator_sucessful_parks": self.activator_sucessful_parks,
            "activator_sucessful_activations": self.activator_sucessful_activations,
            "activator_sucessful_qsos": self.activator_sucessful_qsos,
            "activator_attempted_parks": self.activator_attempted_parks,
            "activator_attempted_activations": self.activator_attempted_activations,
            "activator_attempted_qsos": self.activator_attempted_qsos,
            "hunter_parks": self.hunter_parks,
            "hunter_qsos": self.hunter_qsos,
        }