import unittest
import sys
import os

# Adjust path to import core files properly
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from core.data_structure.heap.heap import Heap
from core.data_structure.priority_queue.priority_queue import PriorityQueue


class TestHeap(unittest.TestCase):
    def test_min_heap_order(self):
        h = Heap(is_min_heap=True)
        h.insert(10)
        h.insert(5)
        h.insert(15)
        h.insert(3)
        self.assertEqual(len(h), 4)
        self.assertEqual(h.peek(), 3)
        self.assertEqual(h.extract(), 3)
        self.assertEqual(h.extract(), 5)
        self.assertEqual(h.extract(), 10)
        self.assertEqual(h.extract(), 15)
        self.assertTrue(h.is_empty())

    def test_max_heap_order(self):
        h = Heap(is_min_heap=False)
        h.insert(10)
        h.insert(5)
        h.insert(15)
        h.insert(3)
        self.assertEqual(h.peek(), 15)
        self.assertEqual(h.extract(), 15)
        self.assertEqual(h.extract(), 10)
        self.assertEqual(h.extract(), 5)
        self.assertEqual(h.extract(), 3)
        self.assertTrue(h.is_empty())

    def test_custom_key(self):
        # Heap sorted by string length (Min-Heap)
        h = Heap(key=lambda s: len(s), is_min_heap=True)
        h.insert("banana")
        h.insert("apple")
        h.insert("kiwi")
        self.assertEqual(h.extract(), "kiwi")   # length 4
        self.assertEqual(h.extract(), "apple")  # length 5
        self.assertEqual(h.extract(), "banana") # length 6

    def test_heapify_min_heap(self):
        data = [10, 5, 15, 3, 20, 2]
        h = Heap(is_min_heap=True, initial_data=data)
        self.assertEqual(len(h), 6)
        # Extracting elements should return them in sorted order
        sorted_elements = [h.extract() for _ in range(6)]
        self.assertEqual(sorted_elements, [2, 3, 5, 10, 15, 20])

    def test_heapify_max_heap(self):
        data = [10, 5, 15, 3, 20, 2]
        h = Heap(is_min_heap=False, initial_data=data)
        self.assertEqual(len(h), 6)
        sorted_elements = [h.extract() for _ in range(6)]
        self.assertEqual(sorted_elements, [20, 15, 10, 5, 3, 2])

    def test_heapify_custom_key(self):
        data = ["banana", "apple", "kiwi"]
        h = Heap(key=lambda s: len(s), is_min_heap=True, initial_data=data)
        self.assertEqual(h.extract(), "kiwi")
        self.assertEqual(h.extract(), "apple")
        self.assertEqual(h.extract(), "banana")

    def test_extract_empty_raises(self):
        h = Heap()
        with self.assertRaises(IndexError):
            h.extract()

    def test_peek_empty_raises(self):
        h = Heap()
        with self.assertRaises(IndexError):
            h.peek()


class TestPriorityQueue(unittest.TestCase):
    def test_priority_queue_ops(self):
        pq = PriorityQueue(key=lambda item: item[0], is_min_heap=True)
        pq.enqueue((2, "task B"))
        pq.enqueue((1, "task A"))
        pq.enqueue((3, "task C"))
        self.assertEqual(len(pq), 3)
        self.assertEqual(pq.peek(), (1, "task A"))
        self.assertEqual(pq.dequeue(), (1, "task A"))
        self.assertEqual(pq.dequeue(), (2, "task B"))
        self.assertEqual(pq.dequeue(), (3, "task C"))
        self.assertTrue(pq.is_empty())


if __name__ == '__main__':
    unittest.main()
