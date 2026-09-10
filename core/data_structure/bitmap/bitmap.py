"""
Bitmap Data Structure for tracking memory allocation status.
0 = Free Block
1 = Allocated Block
"""

class Bitmap:
    def __init__(self, size: int):
        if size <= 0:
            raise ValueError("Bitmap size must be greater than zero.")
        self.size = size
        self.bits = [0] * size

    def is_free(self, index: int) -> bool:
        """Check if a specific block is free (0)."""
        self._validate_index(index)
        return self.bits[index] == 0

    def is_range_free(self, start_index: int, length: int) -> bool:
        """Check if a contiguous range of blocks is entirely free."""
        if start_index < 0 or length <= 0 or (start_index + length) > self.size:
            return False
        return all(bit == 0 for bit in self.bits[start_index:start_index + length])

    def allocate_range(self, start_index: int, length: int) -> None:
        """Mark a range of blocks as allocated (1)."""
        if not self.is_range_free(start_index, length):
            raise ValueError(f"Cannot allocate range [{start_index}, {start_index + length}): blocks are occupied or out of bounds.")
        for i in range(start_index, start_index + length):
            self.bits[i] = 1

    def free_range(self, start_index: int, length: int) -> None:
        """Mark a range of blocks as free (0)."""
        if start_index < 0 or length <= 0 or (start_index + length) > self.size:
            raise IndexError("Range is out of bounds or invalid length.")
        for i in range(start_index, start_index + length):
            self.bits[i] = 0

    def find_contiguous_free(self, length: int, start_offset: int = 0) -> int:
        """
        Find the first contiguous range of free blocks of size 'length'
        starting the search from 'start_offset'.
        Returns start index if found, or -1 if not found.
        """
        if length <= 0 or length > self.size:
            return -1
        
        current_streak = 0
        streak_start = -1

        for i in range(start_offset, self.size):
            if self.bits[i] == 0:
                if current_streak == 0:
                    streak_start = i
                current_streak += 1
                if current_streak == length:
                    return streak_start
            else:
                current_streak = 0
                streak_start = -1

        return -1

    def count_free(self) -> int:
        """Count total number of free blocks (0s)."""
        return self.bits.count(0)

    def count_allocated(self) -> int:
        """Count total number of allocated blocks (1s)."""
        return self.bits.count(1)

    def to_list(self) -> list:
        """Return a copy of the bit list for visualization."""
        return list(self.bits)

    def _validate_index(self, index: int) -> None:
        if index < 0 or index >= self.size:
            raise IndexError(f"Index {index} out of bounds for bitmap of size {self.size}.")