from fr.dasshydro.dassflow2d_py.input.file_reading import *
from fr.dasshydro.dassflow2d_py.d2dtime.TimeStepState import Node

class InitialStateReader:

    def __init__(self):
        pass

    def read(self, file_path: str, number_of_cells: int) -> list[Node]:
        node_list = []
        with open(file_path, 'r') as file:
            for _ in range(number_of_cells):
                h, u, v = extract(file, (float, float, float))
                node = Node(h, u, v)
                node_list.append(node)
        return node_list
