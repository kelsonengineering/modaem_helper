"""
modaem_helper/$/$

Copyright (c) .year Vic Kelson, Kelson Engineering LLC
All Rights Reserved

$

"""

from dataclasses import dataclass

from ..aem_element import Builder, BaseElement, BasePackage


@dataclass
class ReferenceField(BaseElement):
    """
    Contains the reference point of the model, if provided
    """
    x_ref: float = 0.0          # Reference point x
    y_ref: float = 0.0          # Reference point y
    h_ref: float = 1.0          # Reference point head
    dhdx: float = 0.0           # Reference hydraulic gradient
    orientation: float = 0.0    # Reference gradient orientation (in degrees)


class AquiferBoundaryElement(BaseElement):
    """
    Contains a string that makes up a portion of the outer boundary of the model
    """
    ...

class AquiferBoundaryCollection(Builder):
    """
    Contains all the aquifer boundary elements
    """
    element_type = AquiferBoundaryElement

    def __init__(self, )

class Inhomogeneities(Builder):
    domains: list[BaseElement]

class Aquifer(Builder):
    z_bottom: float = 0.0       # Bottom elevation
    z_top: float = 1.0          # Top elevation
    kaq: float = 1.0            # Hydraulic conductivity
    porosity: float = 0.2       # Formation porosity


