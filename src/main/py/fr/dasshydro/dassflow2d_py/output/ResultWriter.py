from fr.dasshydro.dassflow2d_py.d2dtime.TimeStepState import TimeStepState

class ResultWriter:
    """
    Manage program outputs along it's simulation time, this class is supposed to know when and how to write
    TimeStepState results
    """

    def __init__(self, result_file_path: str, delta_to_write: float,):
        raise NotImplementedError("Not yet implemented.")
    
    def isTimeToWrite(self, current_simulation_time: float) -> bool:
        raise NotImplementedError("Not yet implemented.")
    
    def write(self, time_step_state: TimeStepState):
        raise NotImplementedError("Not yet implemented.")
