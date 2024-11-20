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


class Aquifer(BaseElement):
    """
    Contains the aquifer definition information, including inhomogeneity information
    """


@dataclass
class ReferenceField:
    """
    Contains the reference point of the model, if provided
    """
    x_ref: float = 0.0          # Reference point x
    y_ref: float = 0.0          # Reference point y
    h_ref: float = 1.0          # Reference point head
    dhdx: float = 0.0           # Reference hydraulic gradient
    orientation: float = 0.0    # Reference gradient orientation (in degrees)


class Model(BaseModel):
    """
    Contains a aem_helper groundwater flow model.
    """
    z_bottom: float = 0.0                           # Bottom elevation of the infinite aquifer
    z_top: float = 1.0                              # Top elevation of the infinite aqujfer
    k: float = 1.0                                  # Hydraulic conductivity of the infinite aquifer
    n_e: float = 0.2                                # Effective porosity of the infinite aquifer
    reference_field: ReferenceField | None = None   # Reference flow field, if provided
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


