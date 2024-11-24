"""
aem_helper/$/$

Copyright (c) .year Vic Kelson, Kelson Engineering LLC
All Rights Reserved

$

"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Generator
from math import pi

from ..aem_io import Shape
from ..aem_element import BaseElement
from ..aem_model import BaseModel
from .aquifer import Aquifer


class Model(BaseModel):
    """
    Contains a aem_helper groundwater flow model.
    """
    last_id: int | None = None                      # The last element ID assigned in the Model

    def __init__(self, z_bottom: float, z_top: float,
                 k: float, n_e: float,
                 reference_field: ReferenceField = None) -> None:
        super().__init__()
        self.z_bottom = z_bottom
        self.z_top = z_top
        self.k = k
        self.n_e = n_e
        self.reference_field = reference_field

    def header(self) -> Generator[str, None, None]:
        yield "aem\n"

    def trailer(self) -> Generator[str, None, None]:
        yield "eod\n"
