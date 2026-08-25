class Node:
    """A Node in a Doubly Linked List."""
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None


class Queue:
    """
    A FIFO Queue implemented using a custom Doubly Linked List.
    Provides O(1) operations for enqueue and dequeue.
    
    Space Complexity: O(N) where N is the number of elements in the queue.
    """
    def __init__(self):
        self.head = None
        self.tail = None
        self._size = 0

    def enqueue(self, item):
        """
        Add an item to the end of the queue.
        
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        new_node = Node(item)
        if not self.tail:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
        self._size += 1

    def dequeue(self):
        """
        Remove and return the front item.
        
        Raises:
            IndexError: If the queue is empty.
            
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        if self.is_empty():
            raise IndexError("Dequeue from empty queue")
        data = self.head.data
        self.head = self.head.next
        if self.head:
            self.head.prev = None
        else:
            self.tail = None
        self._size -= 1
        return data

    def peek(self):
        """
        Return the front item without removing it.
        
        Raises:
            IndexError: If the queue is empty.
            
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        if self.is_empty():
            raise IndexError("Peek from empty queue")
        return self.head.data

    def is_empty(self) -> bool:
        """
        Check if the queue is empty.
        
        Time Complexity: O(1)
        """
        return self._size == 0

    def __len__(self) -> int:
        """
        Return the number of elements in the queue.
        
        Time Complexity: O(1)
        """
        return self._size
