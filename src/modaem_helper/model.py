"""
modaem_helper/$/$

Copyright (c) .year Vic Kelson, Kelson Engineering LLC
All Rights Reserved

$

"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Generator
from math import pi

from .aem_io import Shape
from .element import Element


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


class Model:
    """
    Contains a modaem_helper groundwater flow model.
    """
    elements: list[Element]                         # All the elements in the model
    element_dict: dict[str, Element]                # A {name: element,...} look-up dict
    z_bottom: float = 0.0                           # Bottom elevation of the infinite aquifer
    z_top: float = 1.0                              # Top elevation of the infinite aqujfer
    k: float = 1.0                                  # Hydraulic conductivity of the infinite aquifer
    n_e: float = 0.2                                # Effective porosity of the infinite aquifer
    reference_field: ReferenceField | None = None   # Reference flow field, if provided

    def __init__(self, z_bottom: float, z_top: float,
                 k: float, n_e: float,
                 reference_field: ReferenceField = None) -> None:
        self.z_bottom = z_bottom
        self.z_top = z_top
        self.k = k
        self.n_e = n_e
        self.reference_field = reference_field
        self.elements = []
        self.element_dict = {}

    def add_element(self, el: Element) -> Element:
        """
        Adds an element to the model, and returns it.

        :param el: The Element to be added. If the element has a not-empty `name`` field, it
            will be added to the model's look-up dictionary
        :return: The added element.
        """
        self.elements.append(el)
        if hasattr(el, "name") and el.name:
            self.element_dict[el.name] = el
        return el

    def get_element(self, name: str) -> Element | None:
        """
        Returns the specified named element
        :param name: The name of the element to be retrieved
        :return: The Element, or None if the name is missing
        """
        return self.element_dict.get(name, None)

    def read_element_shapefile(self,
                               rdr: Generator[Shape],
                               element_type: type[Element]
                               ) -> list[Element]:
        """
        Reads a shapefile of well (WL0) elements and places them in the Model instance.
        :param rdr: A shape generator, e.g.  aem_io.shapefile_reader
        :param element_type: the element type to be created
        :return: A list of all Element objects that were read
        """
        result = []
        for xy, attrs in rdr:
            element = element_type(xy, attrs)
            self.add_element(element)
            result.append(element)
        return result
