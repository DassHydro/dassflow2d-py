import os
from enum import Enum
import h5py #type: ignore
from vtk.util.numpy_support import numpy_to_vtk #type: ignore
import vtk #type: ignore

from fr.dasshydro.dassflow2d_py.d2dtime.TimeStepState import TimeStepState
from fr.dasshydro.dassflow2d_py.mesh.Mesh import Mesh

class OutputMode(Enum):
    VTK = 'vtk',
    TECPLOT = 'tecplot'
    GNUPLOT = 'gnuplot'
    HDF5 = 'hdf5'

class ResultWriter:
    """
    Manage program outputs along it's simulation time, this class is supposed to know when and how to write
    TimeStepState results
    """

    def __init__(self, mesh: Mesh, result_file_path: str, delta_to_write: float):
        if not os.path.exists(result_file_path) or not os.path.isdir(result_file_path):
            raise ValueError("result file folder should be a valid existing folder")
        if delta_to_write <= 0.0:
            raise ValueError("dtw should always be positive and non-zero")
        self.mesh = mesh
        self.result_folder = result_file_path
        self.dtw = delta_to_write
        self.last_quotient = 0
    
    def isTimeToWrite(self, current_simulation_time: float) -> bool:
        quotient = current_simulation_time // self.dtw
        if quotient > self.last_quotient:
            # it's time to write!
            self.last_quotient = int(quotient)
            return True
        return False
    
    def save(self, time_step_state: TimeStepState, current_simulation_time: float):
        """
        This function write raw results contained in the provided time step state.
        These files can be later be used to be converted in vtk, plt, dat, or hdf5 formats

        Args:
            time_step_state (TimeStepState): provided time step state with h, u, and v results
            current_simulation_time (float): simulation time at the write moment
        """
        filename = f"result_{current_simulation_time:.6e}.raw"
        filepath = os.path.join(self.result_folder, filename)

        # write raw results
        with open(filepath, "w") as file:
            for cell in self.mesh.getCells():
                id = cell.getID()
                node_value = time_step_state.getNode(cell)
                h, u, v = node_value.h, node_value.u, node_value.v
                line_to_write = f"{id} {h} {u} {v}\n"
                file.write(line_to_write)

    def _read_raw_file(self, raw_filepath: str):
        ids, hs, us, vs = [], [], [], []
        with open(raw_filepath, "r") as file:
            for line in file:
                parts = line.strip().split()
                ids.append(int(parts[0]))
                hs.append(float(parts[1]))
                us.append(float(parts[2]))
                vs.append(float(parts[3]))
        return ids, hs, us, vs

    def _write_vtk(self, ids, hs, us, vs, filename: str):
        points = vtk.vtkPoints()
        cells = vtk.vtkCellArray()
        h_data = vtk.vtkDoubleArray()
        u_data = vtk.vtkDoubleArray()
        v_data = vtk.vtkDoubleArray()
        h_data.SetName("h")
        u_data.SetName("u")
        v_data.SetName("v")

        for vertex in self.mesh.getVertices():
            vertex_x, vertex_y = vertex.getCoordinates()
            points.InsertNextPoint(vertex_x, vertex_y, 0)

        for cell in self.mesh.getCells():
            cell_vtk = vtk.vtkQuad()
            for i, vertex in enumerate(cell.getVertices()):
                cell_vtk.GetPointIds().SetId(i, vertex.getID() - 1)  # VTK uses 0-based indexing
            cells.InsertNextCell(cell_vtk)

        for i, id in enumerate(ids):
            h_data.InsertNextValue(hs[i])
            u_data.InsertNextValue(us[i])
            v_data.InsertNextValue(vs[i])

        # Create grid
        grid = vtk.vtkUnstructuredGrid()
        grid.SetPoints(points)
        grid.SetCells(vtk.VTK_QUAD, cells)
        grid.GetCellData().AddArray(h_data)
        grid.GetCellData().AddArray(u_data)
        grid.GetCellData().AddArray(v_data)

        # Write as VTK file (version 5.1)
        writer = vtk.vtkUnstructuredGridWriter()
        writer.SetFileTypeToASCII()  # Force ASCII (legacy) format
        writer.SetFileName(filename)
        writer.SetInputData(grid)
        writer.Write()

    def _write_tecplot(self, ids, hs, us, vs, simulation_time: float, filename: str):
        with open(filename, "w") as file:
            file.write('TITLE = "DassFlow Result File in Time"\n')
            file.write('VARIABLES = "x","y","bathy","h","zs","Manning","u","v"\n')

            file.write(
                f'ZONE T = "{simulation_time:.6e}", '
                f'N = {self.mesh.getVertexNumber()}, '
                f'E = {self.mesh.getCellNumber()}, '
                f'DATAPACKING = BLOCK, '
                f'ZONETYPE = FEQUADRILATERAL\n'
            )
            file.write('VARLOCATION = ([3-8]=CELLCENTERED)\n')
            # Write node coordinates
            for vertex in self.mesh.getVertices():
                vertex_x, vertex_y = vertex.getCoordinates()
                file.write(f"{vertex_x} {vertex_y} 0.0\n")
            # Write cell data (simplified for example)
            for i, id in enumerate(ids):
                file.write(f"{hs[i]} {us[i]} {vs[i]} 0.0 0.0 0.0\n")
            # Write connectivity
            for cell in self.mesh.getCells():
                vertices = list(cell.getVertices())
                vertex1_id = vertices[0].getID()
                vertex2_id = vertices[1].getID()
                vertex3_id = vertices[2].getID()
                vertex4_id = vertices[3].getID() if cell.getVerticesNumber() == 4 else 0
                file.write(f"{vertex1_id} {vertex2_id} {vertex3_id} {vertex4_id}\n")

    def _write_gnuplot(self, ids, hs, us, vs, filename: str):
        with open(filename, "w") as file:
            file.write(" # Gnuplot DataFile Version\n")
            file.write(" # i x y bathy h zs Manning u v\n")
            for i, cell in enumerate(self.mesh.getCells()):
                assert cell.getID() == ids[i]
                x = cell.getGravityCenter()[0]
                y = cell.getGravityCenter()[1]
                file.write(f"   {id} {x} {y} 0.0 {hs[i]} {hs[i]} 0.0 {us[i]} {vs[i]}\n")

    def _write_hdf5(self, ids, hs, us, vs, filename: str):
        with h5py.File(filename, "w") as hdf:
            hdf.create_dataset("ids", data=ids)
            hdf.create_dataset("h", data=hs)
            hdf.create_dataset("u", data=us)
            hdf.create_dataset("v", data=vs)
            # Optionally, store mesh data as well

    def writeAll(self, output_mode: OutputMode):
        raw_files = [f for f in os.listdir(self.result_folder) if f.endswith(".raw")]
        for raw_file in raw_files:
            raw_filepath = os.path.join(self.result_folder, raw_file)
            float_str = raw_file.replace("result_", "").replace(".raw", "")
            simulation_time = float(float_str)
            ids, hs, us, vs = self._read_raw_file(raw_filepath)
            base_name = os.path.splitext(raw_file)[0]
            if output_mode == OutputMode.VTK:
                output_file = os.path.join(self.result_folder, f"{base_name}.vtk")
                self._write_vtk(ids, hs, us, vs, output_file)
            elif output_mode == OutputMode.TECPLOT:
                output_file = os.path.join(self.result_folder, f"{base_name}.plt")
                self._write_tecplot(ids, hs, us, vs, simulation_time, output_file)
            elif output_mode == OutputMode.GNUPLOT:
                output_file = os.path.join(self.result_folder, f"{base_name}.dat")
                self._write_gnuplot(ids, hs, us, vs, output_file)
            elif output_mode == OutputMode.HDF5:
                output_file = os.path.join(self.result_folder, f"{base_name}.h5")
                self._write_hdf5(ids, hs, us, vs, output_file)
