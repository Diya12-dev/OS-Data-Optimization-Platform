import unittest
import sys
import os

# Adjust path to import core files properly
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from core.data_structure.queue.queue import Queue
from core.data_structure.circular_queue.circular_queue import CircularQueue


class TestQueue(unittest.TestCase):
    def test_new_queue_is_empty(self):
        q = Queue()
        self.assertTrue(q.is_empty())
        self.assertEqual(len(q), 0)

    def test_enqueue_dequeue(self):
        q = Queue()
        q.enqueue(1)
        q.enqueue(2)
        q.enqueue(3)
        self.assertFalse(q.is_empty())
        self.assertEqual(len(q), 3)
        self.assertEqual(q.peek(), 1)
        self.assertEqual(q.dequeue(), 1)
        self.assertEqual(q.dequeue(), 2)
        self.assertEqual(q.dequeue(), 3)
        self.assertTrue(q.is_empty())
        self.assertEqual(len(q), 0)

    def test_dequeue_empty_raises(self):
        q = Queue()
        with self.assertRaises(IndexError):
            q.dequeue()

    def test_peek_empty_raises(self):
        q = Queue()
        with self.assertRaises(IndexError):
            q.peek()


class TestCircularQueue(unittest.TestCase):
    def test_new_circular_queue_is_empty(self):
        cq = CircularQueue(3)
        self.assertTrue(cq.is_empty())
        self.assertFalse(cq.is_full())
        self.assertEqual(len(cq), 0)

    def test_invalid_capacity(self):
        with self.assertRaises(ValueError):
            CircularQueue(0)
        with self.assertRaises(ValueError):
            CircularQueue(-5)

    def test_enqueue_until_full(self):
        cq = CircularQueue(3)
        self.assertTrue(cq.enqueue("A"))
        self.assertTrue(cq.enqueue("B"))
        self.assertTrue(cq.enqueue("C"))
        self.assertFalse(cq.enqueue("D"))  # Full
        self.assertTrue(cq.is_full())
        self.assertEqual(len(cq), 3)

    def test_dequeue_wrap_around(self):
        cq = CircularQueue(3)
        cq.enqueue("A")
        cq.enqueue("B")
        cq.enqueue("C")
        self.assertEqual(cq.dequeue(), "A")
        self.assertFalse(cq.is_full())
        self.assertTrue(cq.enqueue("D"))  # Wrap around
        self.assertTrue(cq.is_full())
        self.assertEqual(len(cq), 3)
        self.assertEqual(cq.dequeue(), "B")
        self.assertEqual(cq.dequeue(), "C")
        self.assertEqual(cq.dequeue(), "D")
        self.assertTrue(cq.is_empty())

    def test_dequeue_empty_raises(self):
        cq = CircularQueue(3)
        with self.assertRaises(IndexError):
            cq.dequeue()

    def test_peek_empty_raises(self):
        cq = CircularQueue(3)
        with self.assertRaises(IndexError):
            cq.peek()


if __name__ == '__main__':
    unittest.main()
