"""Abstract base classes for phyton"""
from abc import ABC, abstractmethod


class PhytonABC(ABC):  # pylint: disable=too-few-public-methods
    """Abstract base class for phyton"""

    @abstractmethod
    def evaluate(self):
        """Evaluate the module"""


class SoilABC(PhytonABC, ABC):  # pylint: disable=too-few-public-methods
    """Abstract base class for soil module"""


class AtmoABC(PhytonABC, ABC):  # pylint: disable=too-few-public-methods
    """Abstract base class for atmosphere module"""


class PlantABC(PhytonABC, ABC):  # pylint: disable=too-few-public-methods
    """Abstract base class for plant module"""
