from typing import TypeVar, Generic
from abc import ABC, abstractmethod
from mesh.Node import Node
from mesh.Edge import Edge
from mesh.Cell import Cell

T = TypeVar('T', Cell, Edge, Node)
class BoundaryBehavior(ABC, Generic[T]):
    @abstractmethod
    def get_target(self) -> T:
        """Get the target object (Cell, Edge, or Node) associated with the boundary behavior.

        :return: The target object.
        :rtype: T (Cell, Edge, or Node)
        """
        pass
    @abstractmethod
    def get_behavior_type(self) -> str:
        """Get the type of boundary behavior.

        :return: The type of boundary behavior as a string.
        :rtype: str
        """
        pass
    @abstractmethod
    def get_group(self) -> str:
        """Get the group associated with the boundary behavior.

        :return: The indice  group .
        :rtype: int
        """
        pass