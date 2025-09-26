from dassflow2d_py.input.file_reading import extract, next_line
from dassflow2d_py.boundary.BoundaryCondition import BoundaryCondition


class DynamicBoundaryCondition(BoundaryCondition):
    """
    Abstract class representing all boundary conditions that uses a graph file as input and interpolate values
    """

    def _read_dynamic_data(self, filepath: str, dictionary_number: int) -> dict[float, float]:
        """
        Reads a data representing a set of point in a function of time, so the first float represents time
        and the other represent the value of the function at that time

        Args:
            filepath (str): path to the file that contains multiple dynamic data
            dictionary_number (int): index (1-based) of the data in the file

        Raises:
            ValueError: If the index is wrong

        Returns:
            dict[float, float]: mapping of values for every time steps
        """

        with open(filepath, 'r') as file:
            number_of_dictionaries, = extract(file, (int,))
            if dictionary_number > number_of_dictionaries:
                raise ValueError(f"Dictionary number {dictionary_number} is incorrect.")

            # Skip non-relevant hydrographs
            for _ in range(dictionary_number - 1):
                number_of_entries, = extract(file, (int,))
                for _ in range(number_of_entries):
                    next_line(file)

            # Read the correct hydrograph
            dictionary = {}
            number_of_entries, = extract(file, (int,))
            for _ in range(number_of_entries):
                simulation_time, q = extract(file, (float, float))
                dictionary[simulation_time] = q

        return dictionary

    def __init__(self, configuration, boundaries, filepath_supplier, *args):
        super().__init__(configuration, boundaries, args)
        _, _, dictionary_number_arg = args
        dictionary_number = int(dictionary_number_arg)
        dynamic_data_filepath = filepath_supplier()
        self.data = self._read_dynamic_data(dynamic_data_filepath, dictionary_number)
        if len(self.data) == 0:
            raise ValueError(f"No entry has been read in file {dynamic_data_filepath} for dictionary number {dictionary_number}")

    def interpolate_dynamic_value(self, current_simulation_time: float) -> float:
        """
        Linearly interpolate a value from a set of points representing a function of time as input

        Args:
            current_simulation_time (float): the time at which we want to know the value by interpolation

        Returns:
            float: the interpolated value
        """

        # If there is only one entry in data dict, then don't interpolate and return this constant
        if len(self.data) == 1:
            # return the only entry's value
            return next(iter(self.data.values()))

        # Get the time intervals from data dict keys
        times = sorted(self.data.keys())
        number_of_times = len(times)

        # If current simulation time is outside the range, use the closest boundary
        last_time = times[number_of_times-1]
        if current_simulation_time < times[0]:
            t0, t1 = times[0], times[1]
        elif current_simulation_time > last_time:
            t0, t1 = times[number_of_times-2], last_time
        # Find the two closest times
        else:
            t0, t1 = times[0], times[1]
            for i in range(len(times) - 1):
                if times[i] <= current_simulation_time <= times[i + 1]:
                    t0, t1 = times[i], times[i + 1]
                    break

        v0 = self.data[t0]
        v1 = self.data[t1]

        # Linear interpolation
        return v0 + (v1 - v0) * (current_simulation_time - t0) / (t1 - t0)
