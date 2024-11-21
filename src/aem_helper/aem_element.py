"""
aem_helper/$/$

Copyright (c) .year Vic Kelson, Kelson Engineering LLC
All Rights Reserved

$

"""

from __future__ import annotations
from abc import abstractmethod
from typing import Generator, Any, List
from itertools import chain, filter

from .aem_io import ShapeXy, ShapeAttrs, INDENT


class Builder:
    """
    A mix-in class for objects that need to be able to write output elements, either by generating
    a sequence of text strings or by manufacturing objects. This mix-in provides a build() method
    that processes generators header(), body(), and trailer() to build the preprocessor output.

    Builder.build() is a generator that yields the sequence from the other generators, automatically
    skipping entries that are None. If a Builder-derived class yields None, it will be skipped. By
    default, the base-class behavior will yield up nothing; simply override header(), body(), and
    trailer() in derived classes.
    """

    def header(self) -> Generator[str, None, None]:
        """
        Yields the element's header record (if any)
        """
        yield None

    def body(self) -> Generator[str, None, None]:
        """
        Yields a sequence of the element's internal records
        """
        yield None

    def footer(self) -> Generator[str, None, None]:
        """
        Yields the element's end record, if any. By default, this is an empty string
        """
        yield None

    def build(self, element_id: int) -> Generator[str, None, None]:
        """
        Yields up a sequence of text entries corresponding to the input data for the element.
        For example, in ModAEM or GFLOW this would yield one or more strings as a sequence,
        for TimML or TTim, it would yield text that contains Python code.
        """
        yield from filter(lambda z: z is not None,
                          chain([self.header(), self.body(), self.footer()]))


class BaseElement(Builder):
    """
    Base class for aem_helper elements.
    """
    def __init__(self, xy: ShapeXy, attrs: ShapeAttrs, config: dict[str, Any]):
        """
        Initialize the element. The Model object containing the Element will set the element_id.
        :param xy: Geometry of the Element
        :param attrs: Attributes of the Element from model input
        :param config: Configuration dict for the model
        """
        self.element_id = None
        self.xy = self.validate_xy(xy)
        self.process_attrs(attrs, config)

    def set_element_id(self, element_id: int) -> None:
        """
        Sets the element_id for the element.
        :param element_id: Value of the element_id
        """
        self.element_id = element_id

    @staticmethod
    @abstractmethod
    def validate_xy(xy: ShapeXy) -> ShapeXy:
        """
        Validates the (x, y) pairs for the element, raising an exception on error, and stores
        the result in the element..
        :param xy:
        :return:
        """
        ...

    @abstractmethod
    def process_attrs(self, attrs: dict[str, Any], config: dict[str, Any]) -> None:
        """
        Processes the provided attributes for the shape, setting local Element attributes.
        :param attrs: A {name: value} dict for attributes read from model input
        :param config: A {name: value} dict for the model configuration
        :return: Nothing - this method sets local Element attributes.
        """
        ...


class BaseElementCollection(Builder):
    """
    Contains a list of elements, all the same type, for generating model input.
    """
    element_type: type[BaseElement]
    elements: List[BaseElement]

    def __init__(self, source_elements: list[BaseElement]):
        self.elements = [element for element in source_elements if type(element) is self.element_type]
