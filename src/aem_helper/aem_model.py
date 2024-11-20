"""
aem_helper/$/$

Copyright (c) .year Vic Kelson, Kelson Engineering LLC
All Rights Reserved

$

"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Generator, Any
from math import pi

from .aem_io import Shape
from .aem_element import BaseElement, BaseElementCollection

# ElementClasses is a dict of friendly_name: (ElementType, ElementCollectionType)
ElementClasses = dict[str, tuple[type[BaseElement], type[BaseElementCollection]]]

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


class BaseModel:
    """
    Contains a aem_helper groundwater flow model.
    """
    elements: list[BaseElement]                         # All the elements in the model
    element_dict: dict[str, BaseElement]                # A {name: element,...} look-up dict
    supported_elements: ElementClasses                  # Elements and collections for this type
    last_id: int | None = None                          # The most-recently assigned element_id

    def __init__(self, supported_elements: ElementClasses) -> None:
        self.elements = []
        self.element_dict = {}
        self.supported_elements = supported_elements

    def add_element(self, el: BaseElement) -> BaseElement:
        """
        Adds an element to the model, and returns it.

        :param el: The BaseElement to be added. If the element has a not-empty `name`` field, it
            will be added to the model's look-up dictionary
        :return: The added element.
        """
        self.elements.append(el)
        if hasattr(el, "name") and el.name:
            self.element_dict[el.name] = el
        return el

    def get_element(self, name: str) -> BaseElement | None:
        """
        Returns the specified named element
        :param name: The name of the element to be retrieved
        :return: The BaseElement, or None if the name is missing
        """
        return self.element_dict.get(name, None)

    def read_element_shapefile(self,
                               rdr: Generator[Shape],
                               element_type: type[BaseElement]
                               ) -> list[BaseElement]:
        """
        Reads a shapefile of well (WL0) elements and places them in the Model instance.
        :param rdr: A shape generator, e.g.  aem_io.shapefile_reader
        :param element_type: the element type to be created
        :return: A list of all BaseElement objects that were read
        """
        result = []
        for xy, attrs in rdr:
            element = element_type(xy, attrs)
            self.add_element(element)
            result.append(element)
        return result

    def body(self) -> Generator[Any, None, None]:
        """
        Yields up all of the entries in the model's body output.
        :return: A generator of the header elements
        """
        for element_type, collection_type in self.supported_elements.items():
            collection = collection_type(self.elements)
            yield from collection.build()
