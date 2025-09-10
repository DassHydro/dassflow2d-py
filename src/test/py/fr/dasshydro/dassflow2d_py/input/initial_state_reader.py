import unittest
import os
import glob
import yaml

from fr.dasshydro.dassflow2d_py.input.InitialStateReader import InitialStateReader

class TestInitialStateReader(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.base_path = os.path.join('src', 'test', 'resources', 'input')
        cls.test_files = glob.glob(os.path.join(cls.base_path, 'dof_init*.txt'))
        cls.reader = InitialStateReader()
        # Create a list of (test_file, oracle_file) tuples
        cls.test_cases = []
        for test_file in cls.test_files:
            filename = os.path.basename(test_file).split('.')[0]
            oracle_file = os.path.join(cls.base_path, f'{filename}.orcl')
            cls.test_cases.append((test_file, oracle_file))

    def testRead(self):
        for test_file, oracle_file in self.test_cases:
            with open(oracle_file, 'r') as f:
                oracle_data = yaml.safe_load(f)
                number_of_cells = oracle_data['header']['number_of_cells']

            nodes = self.reader.read(test_file, number_of_cells)
            self.assertEqual(len(nodes), number_of_cells)

            for i, node in enumerate(nodes):
                expected_h = oracle_data['nodes'][i]['h']
                expected_u = oracle_data['nodes'][i]['u']
                expected_v = oracle_data['nodes'][i]['v']

                self.assertAlmostEqual(node.h, expected_h)
                self.assertAlmostEqual(node.u, expected_u)
                self.assertAlmostEqual(node.v, expected_v)

if __name__ == '__main__':
    unittest.main()
