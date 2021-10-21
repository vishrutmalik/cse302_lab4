import unittest
import os
from cfg import *
from tac_cfopt import *

dirname, filename = os.path.split(os.path.abspath(__file__))

class testCfgUce(unittest.TestCase):
    def setUp(self):
        fname = "./examples/dead_code.tac.json"

        with open(fname, 'r') as f:
            js_obj = json.load(f)

        proc = js_obj[0]
        new_proc = add_labels_jumps(proc)
        proc_name = new_proc["proc"]
        blocks = proc_to_blocks(new_proc)
        blocks = add_jumps(blocks)
        nodes = create_nodes(blocks)
        self.cfg = CFG(proc_name, nodes)


    def test_edges_init(self):
        expected_edges = {'%.L1': ['%.L4'],
                         '%.L2': ['%.L3'],
                         '%.L3': ['%.L4'],
                         '%.L4': ['%.L5'],
                         '%.L5': []}
        self.assertEqual(self.cfg.edges, expected_edges)

    def test_edges_node_removal(self):
        self.cfg.delete_node("%.L2")
        self.assertFalse(self.cfg.labels_to_nodes["%.L2"] in self.cfg.nodes)

    def test_uce_skip_two(self):
        expected_edges = {'%.L1': ['%.L4'],
                          '%.L4': ['%.L5'],
                          '%.L5': []}
        self.cfg.uce()
        self.assertEqual(self.cfg.edges, expected_edges)
        self.assertEqual(len(self.cfg.nodes), 3)

    def tearDown(self):
        del self.cfg


if __name__ == "__main__":
    unittest.main()
