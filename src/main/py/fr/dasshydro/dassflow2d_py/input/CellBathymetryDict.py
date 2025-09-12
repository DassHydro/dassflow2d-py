from fr.dasshydro.dassflow2d_py.mesh.Mesh import Cell

class CellBathymetryDict(dict[Cell, float]):

    def __init__(self, id_to_bathymetry: dict[int, float]):
        self._data = id_to_bathymetry  # Reference to the original dict

    def __getitem__(self, cell: Cell) -> float:
        return self._data.__getitem__(cell.getID())

    def __contains__(self, cell) -> bool:
        return self._data.__contains__(cell.getID())

    def __len__(self) -> int:
        return self._data.__len__()

    def __setitem__(self, cell: Cell, value: float):
        self._data.__setitem__(cell.getID(), value)
