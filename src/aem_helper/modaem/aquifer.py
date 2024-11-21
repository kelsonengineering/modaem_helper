"""
modaem_helper/$/$

Copyright (c) .year Vic Kelson, Kelson Engineering LLC
All Rights Reserved

$

"""

from dataclasses import dataclass
from typing import Any

from ..aem_io import ShapeXy, ShapeAttrs
from ..aem_element import Builder, BaseElement, BaseElementCollection


@dataclass
class ReferenceField(BaseElement):
    """
    Contains the reference point of the model, if provided
    """
    xy: tuple[float, float]     # Reference point x
    y_ref: float = 0.0          # Reference point y
    h_ref: float = 1.0          # Reference point head
    dhdx: float = 0.0           # Reference hydraulic gradient
    orientation: float = 0.0    # Reference gradient orientation (in degrees)

    @staticmethod
    def validate_xy(xy: ShapeXy) -> ShapeXy:
        return xy[0:1]

    def process_attrs(self, attrs: dict[str, Any], config: dict[str, Any]) -> None:
        self.h_ref =



class AquiferBoundaryElement(BaseElement):
    """
    Contains a string that makes up a portion of the outer boundary of the model
    """

    @staticmethod
    def validate_xy(xy: ShapeXy) -> ShapeXy:
        """
        Validates the (x, y) pairs for the element, raising an exception on error, and stores
        the result in the element..
        :param xy:
        :return:
        """
        ...

    def process_attrs(self, attrs: dict[str, Any], config: dict[str, Any]) -> None:
        """
        Processes the provided attributes for the shape, setting local Element attributes.
        :param attrs: A {name: value} dict for attributes read from model input
        :param config: A {name: value} dict for the model configuration
        :return: Nothing - this method sets local Element attributes.
        """
        ...



class AquiferBoundaryCollection(Builder):
    """
    Contains all the aquifer boundary elements
    """
    element_type = AquiferBoundaryElement

    def __init__(self):
        ...


class InhomogeneityDomainElement(BaseElement):
    """
    Contains an inhomogeneity domain
    """

    @staticmethod
    def validate_xy(xy: ShapeXy) -> ShapeXy:
        """
        Validates the (x, y) pairs for the element, raising an exception on error, and stores
        the result in the element..
        :param xy:
        :return:
        """
        ...

    def process_attrs(self, attrs: dict[str, Any], config: dict[str, Any]) -> None:
        """
        Processes the provided attributes for the shape, setting local Element attributes.
        :param attrs: A {name: value} dict for attributes read from model input
        :param config: A {name: value} dict for the model configuration
        :return: Nothing - this method sets local Element attributes.
        """
        ...


class InhomogeneityDomainCollection(Builder):
    element_type = InhomogeneityDomainElement
    ...


class InhomogenmeityStringElement(BaseElement):

    @staticmethod
    def validate_xy(xy: ShapeXy) -> ShapeXy:
        """
        Validates the (x, y) pairs for the element, raising an exception on error, and stores
        the result in the element..
        :param xy:
        :return:
        """
        ...

    def process_attrs(self, attrs: dict[str, Any], config: dict[str, Any]) -> None:
        """
        Processes the provided attributes for the shape, setting local Element attributes.
        :param attrs: A {name: value} dict for attributes read from model input
        :param config: A {name: value} dict for the model configuration
        :return: Nothing - this method sets local Element attributes.
        """
        ...


class InhomogeneityStringCollection(Builder):
    element_type = InhomogenmeityStringElement
    ...


class Inhomogeneities(Builder):
    domains: InhomogeneityDomainCollection
    strings: InhomogeneityStringCollection

    ...


class Aquifer(BaseElementCollection):
    z_bottom: float = 0.0                   # Bottom elevation
    z_top: float = 1.0                      # Top elevation
    kaq: float = 1.0                        # Hydraulic conductivity
    porosity: float = 0.2                   # Formation porosity
    reference_field: ReferenceField | None = None
    boundary: AquiferBoundaryCollection | None = None
    inhomogeneities: Inhomogeneities | None = None


