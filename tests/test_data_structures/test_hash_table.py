import unittest
from core.data_structure.hash_table.hash_table import HashTable

class TestHashTable(unittest.TestCase):
    def setUp(self):
        self.ht = HashTable(initial_capacity=4, load_factor_threshold=0.75)

    def test_put_and_get(self):
        self.ht.put("page_1", 100)
        self.ht.put("page_2", 200)
        self.assertEqual(self.ht.get("page_1"), 100)
        self.assertEqual(self.ht.get("page_2"), 200)
        self.assertIsNone(self.ht.get("page_unknown"))

    def test_overwrite_existing_key(self):
        self.ht.put("key", 1)
        self.assertEqual(self.ht.get("key"), 1)
        self.assertEqual(len(self.ht), 1)

        self.ht.put("key", 99)
        self.assertEqual(self.ht.get("key"), 99)
        self.assertEqual(len(self.ht), 1)

    def test_remove(self):
        self.ht.put("A", 10)
        self.ht.put("B", 20)
        self.assertTrue(self.ht.contains("A"))

        removed = self.ht.remove("A")
        self.assertTrue(removed)
        self.assertFalse(self.ht.contains("A"))
        self.assertIsNone(self.ht.get("A"))
        self.assertEqual(len(self.ht), 1)

        # Removing non-existent key returns False
        self.assertFalse(self.ht.remove("A"))

    def test_resize(self):
        initial_cap = self.ht.capacity
        # Add items to trigger resize (threshold is 4 * 0.75 = 3 items)
        self.ht.put("k1", 1)
        self.ht.put("k2", 2)
        self.ht.put("k3", 3)
        self.ht.put("k4", 4)

        self.assertGreater(self.ht.capacity, initial_cap)
        # All items must still be accessible after resize
        self.assertEqual(self.ht.get("k1"), 1)
        self.assertEqual(self.ht.get("k2"), 2)
        self.assertEqual(self.ht.get("k3"), 3)
        self.assertEqual(self.ht.get("k4"), 4)

    def test_keys_and_values(self):
        self.ht.put("x", 10)
        self.ht.put("y", 20)
        self.assertCountEqual(self.ht.keys(), ["x", "y"])
        self.assertCountEqual(self.ht.values(), [10, 20])

if __name__ == "__main__":
    unittest.main()