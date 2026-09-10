"""
Hash Table Data Structure
Implements separate chaining for collision resolution and dynamic resizing.
Used for O(1) page lookups in LRU cache and memory mapping.
"""

from typing import Any, Optional, List, Tuple


class HashTable:
    """
    Hash Table with separate chaining.
    """
    def __init__(self, initial_capacity: int = 16, load_factor_threshold: float = 0.75):
        if initial_capacity <= 0:
            raise ValueError("Initial capacity must be greater than zero.")
        self.capacity = initial_capacity
        self.load_factor_threshold = load_factor_threshold
        self.buckets: List[List[Tuple[Any, Any]]] = [[] for _ in range(self.capacity)]
        self._size = 0

    def __len__(self) -> int:
        return self._size

    def _hash(self, key: Any) -> int:
        return hash(key) % self.capacity

    def put(self, key: Any, value: Any) -> None:
        """Insert or update a key-value pair."""
        bucket_index = self._hash(key)
        bucket = self.buckets[bucket_index]

        for i, (existing_key, _) in enumerate(bucket):
            if existing_key == key:
                bucket[i] = (key, value)
                return

        bucket.append((key, value))
        self._size += 1

        if (self._size / self.capacity) > self.load_factor_threshold:
            self._resize(self.capacity * 2)

    def get(self, key: Any) -> Optional[Any]:
        """Retrieve value by key. Returns None if not found."""
        bucket_index = self._hash(key)
        bucket = self.buckets[bucket_index]

        for existing_key, value in bucket:
            if existing_key == key:
                return value
        return None

    def contains(self, key: Any) -> bool:
        """Check if key exists in the table."""
        return self.get(key) is not None

    def remove(self, key: Any) -> bool:
        """Remove key from the table. Returns True if removed, False otherwise."""
        bucket_index = self._hash(key)
        bucket = self.buckets[bucket_index]

        for i, (existing_key, _) in enumerate(bucket):
            if existing_key == key:
                del bucket[i]
                self._size -= 1
                return True
        return False

    def keys(self) -> List[Any]:
        """Return all keys."""
        all_keys = []
        for bucket in self.buckets:
            for k, _ in bucket:
                all_keys.append(k)
        return all_keys

    def values(self) -> List[Any]:
        """Return all values."""
        all_values = []
        for bucket in self.buckets:
            for _, v in bucket:
                all_values.append(v)
        return all_values

    def _resize(self, new_capacity: int) -> None:
        """Rehash all existing items into a new larger bucket array."""
        old_buckets = self.buckets
        self.capacity = new_capacity
        self.buckets = [[] for _ in range(new_capacity)]
        self._size = 0

        for bucket in old_buckets:
            for k, v in bucket:
                self.put(k, v)