from typing import Iterable

from fr.dasshydro.dassflow2d_py.mesh.Mesh import Cell

class Node:

    def __init__(self, h: float, u: float, v: float):
        self.h = h
        self.u = u
        self.v = v


class TimeStepState:

    def __init__(self, state: dict[Cell, Node]):
        self.state = state

    def getNode(self, cell: Cell) -> Node:
        return self.state[cell]
