class Heap:
    """
    A Binary Heap implementation supporting Min-Heap and Max-Heap behavior.
    Represented internally using a dynamic array (Python list).
    
    Space Complexity: O(N) where N is the number of elements in the heap.
    """
    def __init__(self, key=None, is_min_heap=True, initial_data=None):
        """
        Initialize the heap.
        
        Args:
            key (callable, optional): A function to extract a comparison key from each element.
                                      Defaults to lambda x: x.
            is_min_heap (bool, optional): If True, implements a Min-Heap. If False, a Max-Heap.
            initial_data (iterable, optional): Initial collection of elements to heapify in O(N) time.
        """
        self.heap = list(initial_data) if initial_data is not None else []
        self.key = key if key is not None else lambda x: x
        self.is_min_heap = is_min_heap

        if initial_data is not None:
            self.heapify()

    def _compare(self, val1, val2) -> bool:
        """
        Helper to compare two elements according to the heap type (Min vs Max).
        """
        k1 = self.key(val1)
        k2 = self.key(val2)
        if self.is_min_heap:
            return k1 < k2
        return k1 > k2

    def _parent(self, i: int) -> int:
        return (i - 1) // 2

    def _left_child(self, i: int) -> int:
        return 2 * i + 1

    def _right_child(self, i: int) -> int:
        return 2 * i + 2

    def _sift_up(self, i: int):
        """Sift up the element at index i to restore heap property."""
        while i > 0:
            p = self._parent(i)
            if self._compare(self.heap[i], self.heap[p]):
                self.heap[i], self.heap[p] = self.heap[p], self.heap[i]
                i = p
            else:
                break

    def _sift_down(self, i: int):
        """Sift down the element at index i to restore heap property."""
        n = len(self.heap)
        while self._left_child(i) < n:
            target = self._left_child(i)
            r = self._right_child(i)
            if r < n and self._compare(self.heap[r], self.heap[target]):
                target = r
            if self._compare(self.heap[target], self.heap[i]):
                self.heap[i], self.heap[target] = self.heap[target], self.heap[i]
                i = target
            else:
                break

    def heapify(self):
        """
        Build the heap bottom-up in-place in O(N) time.
        
        This algorithm visits parent nodes starting from the last non-leaf node 
        ((N // 2) - 1) down to the root node (0) and sifts each parent down. 
        Mathematically, this bottom-up heap construction runs in O(N) time 
        complexity because the work done at each node is proportional to its height, 
        and the sum of heights of all nodes in a binary tree is O(N).
        """
        n = len(self.heap)
        for i in range((n // 2) - 1, -1, -1):
            self._sift_down(i)

    def insert(self, val):
        """
        Insert a new value into the heap.
        
        Time Complexity: O(log N)
        Space Complexity: O(1) auxiliary
        """
        self.heap.append(val)
        self._sift_up(len(self.heap) - 1)

    def extract(self):
        """
        Remove and return the root element of the heap.
        
        Raises:
            IndexError: If the heap is empty.
            
        Time Complexity: O(log N)
        Space Complexity: O(1) auxiliary
        """
        if self.is_empty():
            raise IndexError("Extract from empty heap")
        if len(self.heap) == 1:
            return self.heap.pop()
        root = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._sift_down(0)
        return root

    def peek(self):
        """
        Return the root element without removing it.
        
        Raises:
            IndexError: If the heap is empty.
            
        Time Complexity: O(1)
        """
        if self.is_empty():
            raise IndexError("Peek from empty heap")
        return self.heap[0]

    def is_empty(self) -> bool:
        """Check if the heap is empty."""
        return len(self.heap) == 0

    def __len__(self) -> int:
        """Return the number of elements in the heap."""
        return len(self.heap)
