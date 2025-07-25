

class ResultWriter:

    def __init__(self, delta_to_write: float):
        raise NotImplementedError("Not yet implemented.")
    
    def isTimeToWrite(self, current_simulation_time: float) -> bool:
        raise NotImplementedError("Not yet implemented.")
    
    def write(self):
        raise NotImplementedError("Not yet implemented.")
