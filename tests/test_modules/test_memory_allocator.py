import unittest
from modules.memory_management.allocator import MemoryAllocator

class TestMemoryAllocator(unittest.TestCase):
    def setUp(self):
        # Setup 5 memory partitions: 100, 500, 200, 300, 600
        self.partitions = [100, 500, 200, 300, 600]
        self.allocator = MemoryAllocator(self.partitions)

    def test_first_fit(self):
        # First Fit for 212 should pick block 1 (size 500)
        idx1 = self.allocator.allocate_first_fit("P1", 212)
        self.assertEqual(idx1, 1)

        # First Fit for 417 should pick block 4 (size 600)
        idx2 = self.allocator.allocate_first_fit("P2", 417)
        self.assertEqual(idx2, 4)

        # First Fit for 112 should pick block 2 (size 200)
        idx3 = self.allocator.allocate_first_fit("P3", 112)
        self.assertEqual(idx3, 2)

        # First Fit for 426 should fail (blocks left: 0(100), 3(300))
        idx4 = self.allocator.allocate_first_fit("P4", 426)
        self.assertIsNone(idx4)

    def test_best_fit(self):
        # Best Fit for 212 should pick block 3 (size 300) since waste = 88
        idx1 = self.allocator.allocate_best_fit("P1", 212)
        self.assertEqual(idx1, 3)

        # Best Fit for 417 should pick block 1 (size 500) since waste = 83
        idx2 = self.allocator.allocate_best_fit("P2", 417)
        self.assertEqual(idx2, 1)

        # Best Fit for 112 should pick block 2 (size 200) since waste = 88
        idx3 = self.allocator.allocate_best_fit("P3", 112)
        self.assertEqual(idx3, 2)

        # Best Fit for 426 should pick block 4 (size 600)
        idx4 = self.allocator.allocate_best_fit("P4", 426)
        self.assertEqual(idx4, 4)

    def test_worst_fit(self):
        # Worst Fit for 212 should pick block 4 (size 600)
        idx1 = self.allocator.allocate_worst_fit("P1", 212)
        self.assertEqual(idx1, 4)

        # Worst Fit for 417 should pick block 1 (size 500)
        idx2 = self.allocator.allocate_worst_fit("P2", 417)
        self.assertEqual(idx2, 1)

    def test_next_fit(self):
        # Next Fit for 212 picks block 1 (size 500)
        idx1 = self.allocator.allocate_next_fit("P1", 212)
        self.assertEqual(idx1, 1)

        # Next Fit for 112 starts searching from index 1, picking block 2 (size 200)
        idx2 = self.allocator.allocate_next_fit("P2", 112)
        self.assertEqual(idx2, 2)

    def test_internal_fragmentation(self):
        self.allocator.allocate_first_fit("P1", 250)  # Goes to block 1 (500), frag = 250
        block = self.allocator.blocks[1]
        self.assertEqual(block.internal_fragmentation, 250)

    def test_deallocation(self):
        idx = self.allocator.allocate_first_fit("P1", 100)
        self.assertTrue(self.allocator.blocks[idx].is_allocated)
        success = self.allocator.deallocate(idx)
        self.assertTrue(success)
        self.assertFalse(self.allocator.blocks[idx].is_allocated)

    def test_run_simulation_format(self):
        requests = [
            {"process_id": "P1", "size": 212},
            {"process_id": "P2", "size": 417}
        ]
        result = self.allocator.run_simulation("Best Fit", requests)
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["algorithm"], "Best Fit")
        self.assertIn("metrics", result)
        self.assertIn("visualization_data", result)
        self.assertEqual(len(result["execution_order"]), 2)

if __name__ == "__main__":
    unittest.main()