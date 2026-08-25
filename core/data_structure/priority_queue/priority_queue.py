from core.data_structure.heap.heap import Heap


class PriorityQueue:
    """
    A Priority Queue implementation wrapping the custom Binary Heap.
    
    Space Complexity: O(N) where N is the number of elements.
    """
    def __init__(self, key=None, is_min_heap=True):
        """
        Initialize the Priority Queue.
        
        Args:
            key (callable, optional): Extract a comparison key from each element.
                                      Defaults to lambda x: x.
            is_min_heap (bool, optional): If True, lower key values have higher priority.
                                          If False, higher key values have higher priority.
        """
        self.heap = Heap(key=key, is_min_heap=is_min_heap)

    def enqueue(self, val):
        """
        Add an item to the priority queue.
        
        Time Complexity: O(log N)
        Space Complexity: O(1) auxiliary
        """
        self.heap.insert(val)

    def dequeue(self):
        """
        Remove and return the highest priority item.
        
        Raises:
            IndexError: If the queue is empty.
            
        Time Complexity: O(log N)
        Space Complexity: O(1) auxiliary
        """
        return self.heap.extract()

    def peek(self):
        """
        Return the highest priority item without removing it.
        
        Raises:
            IndexError: If the queue is empty.
            
        Time Complexity: O(1)
        """
        return self.heap.peek()

    def is_empty(self) -> bool:
        """Check if the priority queue is empty."""
        return self.heap.is_empty()

    def __len__(self) -> int:
        """Return the number of elements in the priority queue."""
        return len(self.heap)
