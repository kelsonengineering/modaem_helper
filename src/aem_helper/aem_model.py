"""
aem_helper/$/$

Copyright (c) .year Vic Kelson, Kelson Engineering LLC
All Rights Reserved

$

"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Generator, Any
from math import pi

from .aem_io import Shape
from .aem_element import Builder, BaseElement, BaseElementCollection


class BaseModel(Builder):
    """
    Contains an aem_helper preprocessor for ModAEM groundwater flow models.
    """
    elements: list[BaseElement]                                 # All the elements in the model
    element_dict: dict[str, BaseElement]                        # A {name: element,...} look-up dict
    supported_elements: dict[str, type[BaseElementCollection]]  # Elements and collections for this type
    last_element_id: int                                        # The most-recently assigned element_id

    def __init__(self, supported_elements: ElementClasses) -> None:
        self.elements = []
        self.element_dict = {}
        self.supported_elements = supported_elements
        self.last_element_id: int = 0

    def add_element(self, el: BaseElement) -> BaseElement:
        """
        Adds an element to the model, and returns it.

        :param el: The BaseElement to be added. If the element has a not-empty `name`` field, it
            will be added to the model's look-up dictionary
        :return: The added element.
        """
        self.set_element_id(el)
        self.elements.append(el)
        if hasattr(el, "name") and el.name:
            self.element_dict[el.name] = el
        return el

    def set_element_id(self, element: BaseElement):
        """
        Generates a new, unique id for the given element
        :param element: The element that will receive a new element_id
        """
        self.last_element_id += 1
        element.set_id(self.last_element_id)

    def get_element(self, name: str) -> BaseElement | None:
        """
        Returns the specified named element
        :param name: The name of the element to be retrieved
        :return: The BaseElement, or None if the name is missing
        """
        return self.element_dict.get(name, None)

    def read_element_shapefile(self, element_name: str, rdr: Generator[Shape]) -> list[BaseElement]:
        """
        Reads a shapefile of well (WL0) elements and places them in the Model instance.
        :param rdr: A shape generator, e.g.  aem_io.shapefile_reader
        :param element_name: the element name that keys into self.supported_elements
        :return: A list of all BaseElement objects that were read
        """
        result = []
        element_collection = self.supported_elements.get(element_name, None)
        if element_collection is None:
            logging.fatal(f"No such element [{element_name}] in ModAEM models")
        for xy, attrs in rdr:
            element = element_collection.element_type(xy, attrs)
            self.add_element(element)
            result.append(element)
        return result

    def body(self) -> Generator[Any, None, None]:
        """
        Yields up all of the entries in the model's body output.
        :return: A generator of the header elements
        """
        for element_type, collection_type in self.supported_elements.values():
            collection = collection_type(self.elements)
            yield from collection.build()
