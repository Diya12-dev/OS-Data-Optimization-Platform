class CircularQueue:
    """
    A FIFO Circular Queue implemented using a fixed-size list.
    Provides O(1) operations for enqueue and dequeue.
    
    Space Complexity: O(N) where N is the capacity of the queue.
    """
    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError("Capacity must be greater than 0")
        self.capacity = capacity
        self.queue = [None] * capacity
        self.head = -1
        self.tail = -1

    def is_full(self) -> bool:
        """
        Check if the circular queue is full.
        
        Time Complexity: O(1)
        """
        return (self.tail + 1) % self.capacity == self.head

    def is_empty(self) -> bool:
        """
        Check if the circular queue is empty.
        
        Time Complexity: O(1)
        """
        return self.head == -1

    def enqueue(self, item) -> bool:
        """
        Add an item to the circular queue.
        Returns True if successful, False if queue is full.
        
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        if self.is_full():
            return False
        if self.is_empty():
            self.head = 0
            self.tail = 0
        else:
            self.tail = (self.tail + 1) % self.capacity
        self.queue[self.tail] = item
        return True

    def dequeue(self):
        """
        Remove and return the front item.
        
        Raises:
            IndexError: If the circular queue is empty.
            
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        if self.is_empty():
            raise IndexError("Dequeue from empty circular queue")
        data = self.queue[self.head]
        self.queue[self.head] = None  # Clear reference for garbage collection
        if self.head == self.tail:
            # Only one element was present, queue is now empty
            self.head = -1
            self.tail = -1
        else:
            self.head = (self.head + 1) % self.capacity
        return data

    def peek(self):
        """
        Return the front item without removing it.
        
        Raises:
            IndexError: If the circular queue is empty.
            
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        if self.is_empty():
            raise IndexError("Peek from empty circular queue")
        return self.queue[self.head]

    def __len__(self) -> int:
        """
        Return the current number of elements in the circular queue.
        
        Time Complexity: O(1)
        """
        if self.is_empty():
            return 0
        if self.tail >= self.head:
            return self.tail - self.head + 1
        return self.capacity - (self.head - self.tail) + 1
