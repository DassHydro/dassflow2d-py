from abc import ABC, abstractmethod 
from mesh.Node import Node
from mesh.Cell import Cell

class Edge(ABC):
    @abstractmethod
    def get_nodes(self) -> list[Node]:
        """Get the list of nodes associated with the edge.

        :return: list of nodes of the edge
        :rtype: list[Node]
        """
        pass

    @abstractmethod
    def get_cells(self) -> list[Cell]:
        """Get the list of cells associated with the edge.

        :return: list of cells associated with the edge
        :rtype: list[Cell]
        """
        pass
    @abstractmethod
    def get_length(self) -> float:
        """Get the length of the edge.

        :return: length of the edge
        :rtype: float
        """
        pass
    @abstractmethod
    def is_boundary(self) -> bool:
        """Check if the edge is on the boundary.

        :return: True if the edge is on the boundary, False otherwise
        :rtype: bool
        """
        pass
    @abstractmethod
    def get_center(self) -> tuple[float, float]:
        """Get the coordinates of the center of the edge.

        :return: coordinates of the center of the edge
        :rtype: tuple[float, float]
        """
        pass
    @abstractmethod
    def get_bridge_vector(self) -> tuple[float, float]:
        """Get the vector connecting the centroids of the two cells adjacent to the edge.

        :return:  coordinates of vector connecting the centroids of the two cells adjacent to the edge (from cell 1 to cell 2).
        :rtype: tuple[float, float]
        """
        pass
    @abstractmethod
    def get_normal_vector(self) -> tuple[float, float]:
        """Get the normal vector of the edge.

        :return: coordinates of the normal vector to the edge  (from cell 1 to cell 2).
        :rtype: tuple[float, float]
        """
        pass
    @abstractmethod
    def get_vector_to_cell(self, cell: Cell) -> tuple[float, float]:
        """Get the vector from the edge to the centroid of a specified cell.

        :param cell: Cell to which the vector is directed.
        :return: coordinates of the vector from the edge to the centroid of the specified cell.
        :rtype: tuple[float, float]
        """
        pass
