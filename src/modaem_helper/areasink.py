"""
modaem_helper/$/$

Copyright (c) .year Vic Kelson, Kelson Engineering LLC
All Rights Reserved

$

"""

from dataclasses import dataclass
from typing import Tuple

from .element import Element

@dataclass
class As0Element(Element):
    """
    A modaem_helper Element for a polygonal area-sink
    """
    xy: Tuple[float, float]
    strength: float
    per_area: bool = False


def read_areasinks(filename: str) -> List[As0Element]:
