from typing import Callable
from io import TextIOWrapper

def _read_next(file: TextIOWrapper, ignore_predicate: Callable[[str], bool]) -> str:
    """Reads the next line in the file that don't match the ignore predicate

    Args:
        file (TextIOWrapper): file to read from
        ignore_predicate (Callable[[str], bool]): predicate on strings that indicate if the line should be ignored
    Returns:
        str: next line that don't match predicate
    """
    line = file.readline()
    while ignore_predicate(line):
        line = file.readline()
        if not line: # EndOfFile reached
            raise EOFError("End of file reached without finding a valid line.")
    return line

def next_line(file: TextIOWrapper) -> str:
    """Gets the next line of text in file ignoring whitespaces and comments

    Args:
        file (TextIOWrapper): file to read line from

    Returns:
        str: the next line in file that is not only whitespaces nor a comment
    """
    def ignore_line(line: str):
        # Strip whitespace from the string
        stripped_line = line.strip()
        # Check if the string is empty or a comment
        return not stripped_line or stripped_line.startswith('#')
    return _read_next(file, ignore_line)

def extract(file: TextIOWrapper, type_tuple: tuple) -> tuple:
    """Extract a number of variables from the next relevant line of a file

    Args:
        file (TextIOWrapper): file to extract relevant line from
        type_tuple (tuple): types of all extracted variables

    Returns:
        tuple: all extracted variables in a tuple
    """
    parts = next_line(file).strip().split()
    return tuple(typ(part) for typ, part in zip(type_tuple, parts))