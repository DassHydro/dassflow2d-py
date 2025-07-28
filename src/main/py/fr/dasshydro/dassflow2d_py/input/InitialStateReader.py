from fr.dasshydro.dassflow2d_py.d2dtime.TimeStepState import TimeStepState

class InitialStateReader:

    def __init__(self):
        raise NotImplementedError("Not yet implemented.")
    
    def read(self, file_path: str) -> TimeStepState:
        raise NotImplementedError("Not yet implemented.")