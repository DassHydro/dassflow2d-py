import unittest
import sys
from io import StringIO
from src.main.py.fr.dasshydro.dassflow2d_py.example import example

class TestExample(unittest.TestCase):

    def test_example(self):
        # redirect stdout to capture the print statement
        captured_output = StringIO()
        sys.stdout = captured_output

        example()

        # reset stdout
        sys.stdout = sys.__stdout__

        # check retrieved value
        self.assertEqual(captured_output.getvalue().strip(), "Hello World!")

if __name__ == '__main__':
    unittest.main()