#
# summit.py - This file is part of DF-TG-Bot
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
from dataclasses import dataclass
from programs.reference import Reference

@dataclass
class Summit(Reference):
    """
    Represents a summit with a name, description, and coordinates.
    """
    points: int
    bonus_points: int

    def __str__(self):
        return super().__str__() + f" - Points: {self.points}, Bonus Points: {self.bonus_points}"

    def to_dict(self):
        """
        Converts the reference to a dictionary format.
        """
        return super().to_dict() | {
            "points": self.points,
            "bonus_points": self.bonus_points
        }
    
if __name__ == "__main__":
    # Example usage
    summit = Summit(
        name="DM/SR-006",
        description="Trautzberg",
        coordinates=(48.137154, 7.576124),
        points=6,
        bonus_points=0
    )
    print(summit)
    print(summit.to_dict())
