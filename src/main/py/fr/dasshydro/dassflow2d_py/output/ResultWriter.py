import os

from fr.dasshydro.dassflow2d_py.d2dtime.TimeStepState import TimeStepState
from fr.dasshydro.dassflow2d_py.mesh.Mesh import Mesh

class ResultWriter:
    """
    Manage program outputs along it's simulation time, this class is supposed to know when and how to write
    TimeStepState results
    """

    def __init__(self, result_file_path: str, delta_to_write: float):
        if not os.path.exists(result_file_path) or not os.path.isdir(result_file_path):
            raise ValueError("result file folder should be a valid existing folder")
        if delta_to_write <= 0.0:
            raise ValueError("dtw should always be positive and non-zero")
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
    
    def write(self, time_step_state: TimeStepState, current_simulation_time: float):
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
            for cell in time_step_state.getKeys():
                id = cell.getID()
                node_value = time_step_state.getNode(cell)
                h, u, v = node_value.h, node_value.u, node_value.v
                line_to_write = f"{id} {h} {u} {v}"
                file.write(line_to_write)
