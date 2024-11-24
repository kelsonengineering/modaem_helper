"""
modaem_helper/$/$

Copyright (c) .year Vic Kelson, Kelson Engineering LLC
All Rights Reserved

$

"""
import logging
from dataclasses import dataclass
from typing import Any, Generator

from ..aem_io import ShapeXy, eval_float, eval_int, eval_object
from ..aem_element import Builder, BaseElement, BaseElementCollection, BasePackage



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
        if len(xy) > 1:
            logging.warn("Only one point in the reference field is allowed. Using the first entry.")
        return xy[0:1]

    def process_attrs(self, attrs: dict[str, Any], config: dict[str, Any]) -> None:
        self.h_ref = eval_float(attrs.get("HEAD", None), config=config)
        self.dhdx = eval_float(attrs.get("SLOPE", None), config=config)
        self.orientation = eval_float(attrs.get("ANGLE", None), config=config)

    def body(self):
        x, y = self.xy[0]
        yield f"ref ({x}, {y}) {self.h_ref} {self.dhdx} {self}\n"


class AquBoundaryElement(BaseElement):
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


class AquBoundaryCollection(BaseElementCollection):
    """
    Contains all the aquifer boundary elements
    """
    element_type = AquBoundaryElement

    def __init__(self, source_elements: list[BaseElement]):
        super().__init__(source_elements)

    @property
    def boundary_count(self) -> int:
        """ Returns the number of boundary elements in the collection
        :return: the number of boundary elements in the collection
        """
        return 0


class In0DomainElement(BaseElement):
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


class In0DomainCollection(BaseElementCollection):
    element_type = In0DomainElement
    ...


class In0StringElement(BaseElement):

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


class In0StringCollection(BaseElementCollection):
    element_type = In0StringElement
    ...


class Inhomogeneities(Builder):
    domains: In0DomainCollection
    strings: In0StringCollection

    def __init__(self, domains: In0DomainCollection, strings: In0StringCollection) -> None:
        self.domains = domains
        self.strings = strings

    @property
    def domain_count(self):
        return 0

    @property
    def string_count(self):
        return 0


class Aquifer(BasePackage):
    z_bottom: float = 0.0                   # Bottom elevation
    z_top: float = 1.0                      # Top elevation
    kaq: float = 1.0                        # Hydraulic conductivity
    porosity: float = 0.2                   # Formation porosity
    reference_field: ReferenceField | None = None
    boundary: AquBoundaryCollection | None = None
    inhomogeneities: Inhomogeneities | None = None

    def __init__(self, source_elements: list[BaseElement]):
        super().__init__(source_elements)

        # Scan for the reference point
        el = [el for el in source_elements if isinstance(el, ReferenceField)]
        if el:
            if len(el) > 1:
                logging.warning("Multiple ReferenceField elements found. Utilizing the first one.")
            self.reference_field = el[0]

        self.boundary = AquBoundaryCollection(source_elements)
        self.inhomogeneities = Inhomogeneities(In0DomainCollection(source_elements),
                                               In0StringCollection(source_elements))

    @property
    def boundary_count(self) -> int:
        return self.boundary.boundary_count

    @property
    def domain_count(self) -> int:
        return self.inhomogeneities.domain_count
    @property
    def string_count(self):
        return self.inhomogeneities.string_count

    def header(self) -> Generator[str, None, None]:
        yield f"aqu {self.boundary_count} {self.domain_count} {self.string_count}\n"

    def trailer(self) -> Generator[str, None, None]:
        yield "end\n"
