import unittest
from modules.memory_management.paging import PageReplacementManager, LRUCache

class TestLRUCacheDirect(unittest.TestCase):
    def test_lru_cache_operations(self):
        cache = LRUCache(3)
        # Put 1, 2, 3
        cache.put(1)
        cache.put(2)
        cache.put(3)
        self.assertEqual(cache.get_frames(), [1, 2, 3])

        # Access 1 (makes 1 most recent -> order becomes [2, 3, 1])
        hit = cache.get(1)
        self.assertTrue(hit)
        self.assertEqual(cache.get_frames(), [2, 3, 1])

        # Put 4 -> should evict least recently used (2)
        evicted = cache.put(4)
        self.assertEqual(evicted, 2)
        self.assertEqual(cache.get_frames(), [3, 1, 4])


class TestPageReplacementManager(unittest.TestCase):
    def setUp(self):
        self.manager = PageReplacementManager(capacity=3)
        # Standard textbook reference string
        self.ref_string = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2]

    def test_fifo_metrics(self):
        result = self.manager.run_fifo(self.ref_string)
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["algorithm"], "FIFO Page Replacement")
        metrics = result["metrics"]
        self.assertEqual(metrics["total_references"], len(self.ref_string))
        self.assertEqual(metrics["page_hits"] + metrics["page_faults"], len(self.ref_string))
        self.assertAlmostEqual(metrics["hit_ratio"] + metrics["fault_ratio"], 1.0, places=3)
        self.assertEqual(len(result["events"]), len(self.ref_string))

    def test_lru_metrics(self):
        result = self.manager.run_lru(self.ref_string)
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["algorithm"], "LRU Page Replacement")
        metrics = result["metrics"]
        self.assertEqual(metrics["total_references"], len(self.ref_string))
        self.assertEqual(metrics["page_hits"] + metrics["page_faults"], len(self.ref_string))
        self.assertAlmostEqual(metrics["hit_ratio"] + metrics["fault_ratio"], 1.0, places=3)

    def test_simple_lru_scenario(self):
        # String: [1, 2, 1, 3] with capacity 2
        mgr = PageReplacementManager(capacity=2)
        res = mgr.run_lru([1, 2, 1, 3])
        # 1: fault [1]
        # 2: fault [1, 2]
        # 1: hit   [2, 1]
        # 3: fault evict 2 -> [1, 3]
        self.assertEqual(res["metrics"]["page_hits"], 1)
        self.assertEqual(res["metrics"]["page_faults"], 3)
        self.assertEqual(res["visualization_data"]["final_frames"], [1, 3])

if __name__ == "__main__":
    unittest.main()