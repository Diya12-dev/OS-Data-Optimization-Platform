import unittest
from modules.memory_management.comparison import MemoryComparisonEngine, PagingComparisonEngine


class TestMemoryComparisonEngine(unittest.TestCase):
    def setUp(self):
        self.partitions = [100, 500, 200, 300, 600]
        self.requests = [
            {"process_id": "P1", "size": 212},
            {"process_id": "P2", "size": 417},
            {"process_id": "P3", "size": 112},
            {"process_id": "P4", "size": 426}
        ]

    def test_compare_allocators(self):
        res = MemoryComparisonEngine.compare_allocators(self.partitions, self.requests)
        self.assertEqual(res["status"], "success")
        self.assertEqual(res["type"], "Contiguous Allocation Comparison")
        self.assertEqual(len(res["comparison_table"]), 4)
        self.assertIn("recommendation", res)
        self.assertIn(res["recommendation"]["recommended_algorithm"], ["First Fit", "Best Fit", "Worst Fit", "Next Fit"])


class TestPagingComparisonEngine(unittest.TestCase):
    def test_compare_paging(self):
        ref_string = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2]
        res = PagingComparisonEngine.compare_paging(capacity=3, reference_string=ref_string)
        self.assertEqual(res["status"], "success")
        self.assertEqual(res["type"], "Page Replacement Comparison")
        self.assertEqual(len(res["comparison_table"]), 2)
        self.assertIn("recommendation", res)
        self.assertIn(res["recommendation"]["recommended_algorithm"], ["LRU", "FIFO", "LRU / FIFO (Tied)"])


if __name__ == "__main__":
    unittest.main()