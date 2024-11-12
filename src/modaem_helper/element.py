"""
modaem_helper/$/$

Copyright (c) .year Vic Kelson, Kelson Engineering LLC
All Rights Reserved

$

"""

from typing import Any, Protocol


class Element(Protocol):
    """
    Base class for modaem_helper elements.
    """
    def __init__(self,
                 xy: list[tuple[float, float]],
                 attrs: dict[str, Any],
                 config: dict[str, Any]):
        ...

