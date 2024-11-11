"""
modaem_helper/$/$

Copyright (c) .year Vic Kelson, Kelson Engineering LLC
All Rights Reserved

$

"""

from __future__ import annotations

from .element import Element
from .well import Wl0Element, Wl1Element
from .linesink import Ls0Element, Ls1Element, Ls2Element
from .areasink import As0Element
from .domain import In0String, In0Domain


class Model:
    """
    Contains a modaem_helper groundwater flow model.
    """
    def __init__(self):
