"""
modaem_helper/$/$

Copyright (c) .year Vic Kelson, Kelson Engineering LLC
All Rights Reserved

$

"""

from __future__ import annotations
from abc import abstractmethod
from typing import Generator, Any
from itertools import chain

from .aem_io import ShapeXy, ShapeAttrs, INDENT


class Element:
    """
    Base class for modaem_helper elements.
    """
    @abstractmethod
    def __init__(self, xy: ShapeXy, attrs: ShapeAttrs, config: dict[str, Any]):
        ...

    @staticmethod
    @abstractmethod
    def _validate_xy(xy: ShapeXy) -> ShapeXy:
        ...

    @abstractmethod
    def header(self) -> Generator[str, None, None]:
        """
        Yields the element's header record (if any)
        """
        ...

    @abstractmethod
    def body(self, element_id: int) -> Generator[str, None, None]:
        """
        Yields a sequence of the element's internal records
        """
        ...

    @abstractmethod
    def footer(self) -> Generator[str, None, None]:
        """
        Yields the element's end record, if any. By default, this is an empty string
        """
        ...

    def to_modaem(self, element_id: int) -> Generator[str, None, None]:
        """
        Yields up a sequence of strings that provide the ModAEM input for this element
        """
        yield from chain(self.header(), self.body(), self.footer())


class ElementCollection:
    """
    Contains a list of elements, all the same type
    """
    def __init__(self, source_elements: list[Element], element_type: type[Element]):
        self.elements = [element for element in source_elements if type(element) is element_type]

    @abstractmethod
    def header(self) -> Generator[str, None, None]:
        """
        Yields the element's header record (if any)
        """
        ...

    def body(self) -> Generator[str, None, None]:
        """
        Yields a sequence of the collection's internal elements
        """
        for element_id, element in enumerate(self.elements):
            yield from (f"{INDENT}{s}" for s in element.body(element_id))

    @abstractmethod
    def footer(self) -> Generator[str, None, None]:
        """
        Yields the element's end record, if any. By default, this is an empty string
        """
        ...

    def to_modaem(self) -> Generator[str, None, None]:
        """
        Yields up a sequence of strings that provide the ModAEM input for this element
        """
        yield from chain(self.header(), self.body(), self.footer())
