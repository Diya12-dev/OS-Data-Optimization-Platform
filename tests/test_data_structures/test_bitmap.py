import unittest
from core.data_structure.bitmap.bitmap import Bitmap

class TestBitmap(unittest.TestCase):
    def test_bitmap_initialization(self):
        bm = Bitmap(8)
        self.assertEqual(bm.size, 8)
        self.assertEqual(bm.count_free(), 8)
        self.assertEqual(bm.count_allocated(), 0)
        self.assertEqual(bm.to_list(), [0, 0, 0, 0, 0, 0, 0, 0])

    def test_bitmap_invalid_initialization(self):
        with self.assertRaises(ValueError):
            Bitmap(0)
        with self.assertRaises(ValueError):
            Bitmap(-5)

    def test_bitmap_allocation_and_free(self):
        bm = Bitmap(8)
        bm.allocate_range(2, 3)
        self.assertEqual(bm.to_list(), [0, 0, 1, 1, 1, 0, 0, 0])
        self.assertTrue(bm.is_free(1))
        self.assertFalse(bm.is_free(2))
        self.assertEqual(bm.count_allocated(), 3)
        self.assertEqual(bm.count_free(), 5)

        bm.free_range(3, 2)
        self.assertEqual(bm.to_list(), [0, 0, 1, 0, 0, 0, 0, 0])
        self.assertEqual(bm.count_allocated(), 1)

    def test_bitmap_out_of_bounds_allocation(self):
        bm = Bitmap(5)
        with self.assertRaises(ValueError):
            bm.allocate_range(3, 4)

    def test_bitmap_double_allocation(self):
        bm = Bitmap(5)
        bm.allocate_range(1, 2)
        with self.assertRaises(ValueError):
            bm.allocate_range(2, 2)

    def test_find_contiguous_free(self):
        bm = Bitmap(10)
        self.assertEqual(bm.find_contiguous_free(4), 0)

        bm.allocate_range(0, 3)
        self.assertEqual(bm.find_contiguous_free(4), 3)

        bm.allocate_range(5, 3)
        self.assertEqual(bm.find_contiguous_free(3), -1)
        self.assertEqual(bm.find_contiguous_free(2), 3)
        self.assertEqual(bm.find_contiguous_free(2, start_offset=4), 8)

if __name__ == "__main__":
    unittest.main()