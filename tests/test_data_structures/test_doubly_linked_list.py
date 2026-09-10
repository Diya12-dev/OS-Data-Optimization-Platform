import unittest
from core.data_structure.doubly_linked_list.doubly_linked_list import DoublyLinkedList, Node

class TestDoublyLinkedList(unittest.TestCase):
    def setUp(self):
        self.dll = DoublyLinkedList()

    def test_initial_state(self):
        self.assertTrue(self.dll.is_empty())
        self.assertEqual(len(self.dll), 0)
        self.assertIsNone(self.dll.pop_first())

    def test_append_and_traverse(self):
        n1 = Node(key="A", value=1)
        n2 = Node(key="B", value=2)
        self.dll.append(n1)
        self.dll.append(n2)

        self.assertEqual(len(self.dll), 2)
        self.assertEqual(
            self.dll.to_list(),
            [{"key": "A", "value": 1}, {"key": "B", "value": 2}]
        )

    def test_pop_first(self):
        n1 = Node(key="A", value=1)
        n2 = Node(key="B", value=2)
        self.dll.append(n1)
        self.dll.append(n2)

        popped = self.dll.pop_first()
        self.assertEqual(popped.key, "A")
        self.assertEqual(len(self.dll), 1)
        self.assertEqual(self.dll.to_list(), [{"key": "B", "value": 2}])

    def test_move_to_end(self):
        n1 = Node(key="A", value=1)
        n2 = Node(key="B", value=2)
        n3 = Node(key="C", value=3)
        self.dll.append(n1)
        self.dll.append(n2)
        self.dll.append(n3)

        # Move A to end -> order should be B, C, A
        self.dll.move_to_end(n1)
        self.assertEqual(
            self.dll.to_list(),
            [{"key": "B", "value": 2}, {"key": "C", "value": 3}, {"key": "A", "value": 1}]
        )

    def test_remove_middle(self):
        n1 = Node(key="A", value=1)
        n2 = Node(key="B", value=2)
        n3 = Node(key="C", value=3)
        self.dll.append(n1)
        self.dll.append(n2)
        self.dll.append(n3)

        self.dll.remove(n2)
        self.assertEqual(len(self.dll), 2)
        self.assertEqual(
            self.dll.to_list(),
            [{"key": "A", "value": 1}, {"key": "C", "value": 3}]
        )

if __name__ == "__main__":
    unittest.main()