from dassflow2d_py.input.file_reading import *
from dassflow2d_py.d2dtime.TimeStepState import Node

class InitialStateReader:

    def __init__(self):
        pass

    def read(self, file_path: str, number_of_cells: int) -> list[Node]:
        """
        Reads an init file with all h, u, and v values for every node at the start of the simulation

        Args:
            file_path (str): string path to the init file
            number_of_cells (int): number of cells in the mesh

        Returns:
            list[Node]: every node read, the nodes are in order such as it maps to a cell list sorted by id
        """
        node_list = []
        with open(file_path, 'r') as file:
            for _ in range(number_of_cells):
                h, u, v = extract(file, (float, float, float))
                node = Node(h, u, v)
                node_list.append(node)
        return node_list
