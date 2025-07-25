from abc import ABC, abstractmethod 
from mesh.Node import Node
from mesh.Edge import Edge
from mesh.Cell import Cell

class Cell(ABC):
    @abstractmethod
    def getgravitycenter(self) -> tuple[float, float]:
        """_summary_

        :return: centre of gravity of the cell
        :rtype: tuple[float, float]
        """
        pass
    @abstractmethod
    def get_nodes(self) -> list[Node]:
        """_summary_

        :return: list of nodes of the cell
        :rtype: list[Nodes]
        """
        pass
    @abstractmethod
    def  get_edges(self) -> list[Edge]:
        """_summary_

        :return: list of edges of the cell
        :rtype: list[Edge]
        """
        pass
    @abstractmethod
    def get_neighbors(self) -> list[Cell]:
        """_summary_

        :return: list of neighboring cells
        :rtype: list[Cell]
        """
        pass
    @abstractmethod
    def get_surface(self) -> float:
        """_summary_

        :return: surface area of the cell
        :rtype: float
        """
        pass
    @abstractmethod
    def get_perimeter(self) -> float:
        """_summary_

        :return: perimeter of the cell
        :rtype: float
        """
        pass
    @abstractmethod
    def is_boundary(self) -> bool:
        """_summary_

        :return: True if the cell is on the boundary, False otherwise
        :rtype: bool
        """
        pass
