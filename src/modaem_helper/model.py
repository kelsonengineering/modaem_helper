"""
modaem_helper/$/$

Copyright (c) .year Vic Kelson, Kelson Engineering LLC
All Rights Reserved

$

"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Union
from math import pi

from .element import Element
from .well import Wl0Element, Wl1Element
from .linesink import Ls0Element, Ls1Element, Ls2Element
from .areasink import As0Element
from .inhomogeneity import In0String, In0Domain


ElementType = Union[Wl0Element,
                    Wl1Element,
                    Ls0Element,
                    Ls1Element,
                    Ls2Element,
                    As0Element,
                    In0String,
                    In0Domain,
                    ]


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


@dataclass
class Model:
    """
    Contains a modaem_helper groundwater flow model.
    """
    elements: list[Element]             # All the elements in the model
    element_dict: dict[str, Element]    # A {name: element,...} look-up dict
    reference_field: ReferenceField | None
    z_bottom: float = 0.0
    z_top: float = 1.0
    k: float = 1.0
    n_e: float = 0.2

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

    def collect_elements(self, element_type: ElementType) -> list[Element]:
        """
        Collects all the elements that match the specified ElementType and returns them
        as a list.
        :param element_type: The type of Element to be collected
        :return: A list of Elements
        """
        return [el for el in self.elements if type(el) is element_type]
