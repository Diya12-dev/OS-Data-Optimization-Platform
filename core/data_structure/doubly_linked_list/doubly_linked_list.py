"""
Doubly Linked List Data Structure
Used for O(1) removals and updates in Page/Cache Replacement (e.g., LRU).
"""

from typing import Any, Optional


class Node:
    """Represents an individual node in a Doubly Linked List."""
    def __init__(self, key: Any, value: Any):
        self.key = key
        self.value = value
        self.prev: Optional['Node'] = None
        self.next: Optional['Node'] = None


class DoublyLinkedList:
    """
    Doubly Linked List with sentinel head and tail nodes.
    Supports O(1) append to tail, remove arbitrary node, and pop head.
    """
    def __init__(self):
        # Sentinel dummy nodes
        self.head = Node(key=None, value=None)
        self.tail = Node(key=None, value=None)
        self.head.next = self.tail
        self.tail.prev = self.head
        self._size = 0

    def __len__(self) -> int:
        return self._size

    def is_empty(self) -> bool:
        return self._size == 0

    def append(self, node: Node) -> None:
        """Add node right before the dummy tail (most recently used position)."""
        prev_node = self.tail.prev
        prev_node.next = node
        node.prev = prev_node
        node.next = self.tail
        self.tail.prev = node
        self._size += 1

    def remove(self, node: Node) -> None:
        """Remove a specific node in O(1) time."""
        if node.prev is None or node.next is None:
            return
        node.prev.next = node.next
        node.next.prev = node.prev
        node.prev = None
        node.next = None
        self._size -= 1

    def pop_first(self) -> Optional[Node]:
        """Remove and return the first real node after head (least recently used)."""
        if self.is_empty():
            return None
        first_real = self.head.next
        self.remove(first_real)
        return first_real

    def move_to_end(self, node: Node) -> None:
        """Move an existing node to the tail (refresh recency)."""
        self.remove(node)
        self.append(node)

    def to_list(self) -> list:
        """Traverse and return key-value pairs from head to tail."""
        result = []
        curr = self.head.next
        while curr != self.tail:
            result.append({"key": curr.key, "value": curr.value})
            curr = curr.next
        return result