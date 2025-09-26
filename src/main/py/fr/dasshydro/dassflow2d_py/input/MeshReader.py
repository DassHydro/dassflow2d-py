from abc import ABC, abstractmethod

from dassflow2d_py.mesh.Mesh import RawCell, RawVertex, RawInlet, RawOutlet


class MeshReader(ABC):

    @abstractmethod
    def read(self, file_path: str) -> tuple[
            list[RawVertex],
            list[RawCell],
            list[RawInlet],
            list[RawOutlet],
            dict[int, float],
            dict[int, float]
        ]:
        """
        Read all information contained in a dassflow mesh.

        Args:
            file_path (str): string path to the mesh file

        Returns:
            tuple[ list[RawVertex], list[RawCell], list[RawInlet], list[RawOutlet], dict[int, float], dict[int, float] ]:
            all information in a tuple
        """
        pass
