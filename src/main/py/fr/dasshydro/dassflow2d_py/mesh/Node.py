from abc import ABC, abstractmethod 
        
class Node(ABC):
    @abstractmethod
    def getCoordinates(self) -> tuple[float, float]:
        """Get the coordinates of the node.

        :return: coordinates of the node
        :rtype: tuple[float, float]
        """
        pass

    @abstractmethod
    def is_boundary(self) -> bool:
        """Check if the node is on the boundary.

        :return: True if the node is on the boundary, False otherwise
        :rtype: bool
        """
        pass
