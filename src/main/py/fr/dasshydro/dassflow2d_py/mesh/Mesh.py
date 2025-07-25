from enum import Enum
from abc import ABC, abstractmethod
from mesh.Node import Node
from mesh.Edge import Edge
from mesh.Cell import Cell
from mesh.BoundaryBehavior import BoundaryBehavior  

class MeshShape(Enum):
    TRIANGULAR = "triangular"
    QUADRILATERAL = "quadrilateral"
    HYBRID = "hybrid"

class MeshType(Enum):
    BASIC = "basic"
    DASSFLOW = "dassflow"


class Mesh(ABC):

    @abstractmethod
    def get_cells(self) -> list[Cell]:
        """Get the list of cells in the mesh.

        :return: List of cells.
        :rtype: list[Cell]
        """
        pass
    @abstractmethod
    def get_cell_number(self) -> int:
        """Get the number of cells in the mesh.

        :return: Number of cells.
        :rtype: int
        """
        pass

    @abstractmethod
    def get_boundary_cell_behaviors(self) -> list[BoundaryBehavior[Cell]]:
        """Get the list of boundary behaviors associated with cells in the mesh.

        :return: List of boundary behaviors.
        :rtype: list[BoundaryBehavior[Cell]]
        """
        pass

    @abstractmethod
    def get_boundary_cell_behavior_number(self) -> int:
        """Get the number of boundary behaviors associated with cells in the mesh.

        :return: Number of boundary behaviors.
        :rtype: int
        """
        pass

    @abstractmethod
    def get_edges(self) -> list[Edge]:
        """Get the list of edges in the mesh.

        :return: List of edges.
        :rtype: list[Edge]
        """
        pass
    @abstractmethod
    def get_edge_number(self) -> int:
        """Get the number of edges in the mesh.

        :return: Number of edges.
        :rtype: int
        """
        pass
    @abstractmethod
    def get_boundary_edge_behaviors(self) -> list[BoundaryBehavior[Edge]]:
        """Get the list of boundary behaviors associated with edges in the mesh.

        :return: List of boundary behaviors.
        :rtype: list[BoundaryBehavior[Edge]]
        """
        pass

    @abstractmethod
    def get_boundary_edge_behavior_number(self) -> int:
        """Get the number of boundary behaviors associated with edges in the mesh.

        :return: Number of boundary behaviors.
        :rtype: int
        """
        pass

    @abstractmethod
    def get_nodes(self) -> list[Node]:
        """Get the list of nodes in the mesh.

        :return: List of nodes.
        :rtype: list[Node]
        """
        pass

    @abstractmethod
    def get_node_number(self) -> int:
        """Get the number of nodes in the mesh.

        :return: Number of nodes.
        :rtype: int
        """
        pass
    @abstractmethod
    def get_surface(self) -> float:
        """Get the total surface area of the mesh.

        :return: Total surface area.
        :rtype: float
        """
        pass
