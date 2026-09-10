"""
Page and Cache Replacement Module
Implements:
- FIFO (First-In-First-Out)
- LRU (Least Recently Used) using custom HashTable + DoublyLinkedList
Calculates:
- Page Hits, Page Faults, Hit Ratio, Fault Ratio
Provides visualization snapshots for each reference step.
"""

from typing import List, Dict, Any
from core.data_structure.doubly_linked_list.doubly_linked_list import DoublyLinkedList, Node
from core.data_structure.hash_table.hash_table import HashTable


class LRUCache:
    """
    O(1) LRU Cache powered by custom HashTable + DoublyLinkedList.
    """
    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError("Cache capacity must be greater than zero.")
        self.capacity = capacity
        self.table = HashTable(initial_capacity=capacity * 2)
        self.dll = DoublyLinkedList()

    def get(self, page: int) -> bool:
        """Check if page exists. If hit, move to end (most recent)."""
        node: Node = self.table.get(page)
        if node is not None:
            self.dll.move_to_end(node)
            return True
        return False

    def put(self, page: int) -> int | None:
        """
        Insert page. If capacity exceeded, evict LRU node from DLL head.
        Returns evicted page number if eviction occurred, else None.
        """
        existing_node: Node = self.table.get(page)
        if existing_node is not None:
            self.dll.move_to_end(existing_node)
            return None

        evicted_page = None
        if len(self.dll) >= self.capacity:
            lru_node = self.dll.pop_first()
            if lru_node:
                evicted_page = lru_node.key
                self.table.remove(evicted_page)

        new_node = Node(key=page, value=page)
        self.dll.append(new_node)
        self.table.put(page, new_node)
        return evicted_page

    def get_frames(self) -> List[int]:
        """Return current pages in cache from least recent to most recent."""
        return [item["key"] for item in self.dll.to_list()]


class PageReplacementManager:
    """
    Page Replacement Simulator supporting FIFO and LRU.
    """
    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError("Frame capacity must be greater than zero.")
        self.capacity = capacity

    def run_fifo(self, reference_string: List[int]) -> Dict[str, Any]:
        """Simulate FIFO page replacement."""
        frames: List[int] = []
        hits = 0
        faults = 0
        events = []
        execution_order = []

        for step, page in enumerate(reference_string):
            is_hit = page in frames
            evicted = None

            if is_hit:
                hits += 1
                status = "HIT"
            else:
                faults += 1
                status = "FAULT"
                if len(frames) >= self.capacity:
                    evicted = frames.pop(0)  # FIFO: remove oldest
                frames.append(page)

            execution_order.append(page)
            events.append({
                "step": step + 1,
                "page": page,
                "status": status,
                "evicted_page": evicted,
                "current_frames": list(frames)
            })

        return self._format_result("FIFO Page Replacement", execution_order, hits, faults, events, frames)

    def run_lru(self, reference_string: List[int]) -> Dict[str, Any]:
        """Simulate LRU page replacement using HashTable + DoublyLinkedList."""
        cache = LRUCache(self.capacity)
        hits = 0
        faults = 0
        events = []
        execution_order = []

        for step, page in enumerate(reference_string):
            is_hit = cache.get(page)
            evicted = None

            if is_hit:
                hits += 1
                status = "HIT"
            else:
                faults += 1
                status = "FAULT"
                evicted = cache.put(page)

            execution_order.append(page)
            events.append({
                "step": step + 1,
                "page": page,
                "status": status,
                "evicted_page": evicted,
                "current_frames": cache.get_frames()
            })

        return self._format_result("LRU Page Replacement", execution_order, hits, faults, events, cache.get_frames())

    def _format_result(
        self,
        algo_name: str,
        execution_order: List[int],
        hits: int,
        faults: int,
        events: List[Dict[str, Any]],
        final_frames: List[int]
    ) -> Dict[str, Any]:
        total_references = hits + faults
        hit_ratio = round(hits / total_references, 4) if total_references > 0 else 0.0
        fault_ratio = round(faults / total_references, 4) if total_references > 0 else 0.0

        return {
            "status": "success",
            "algorithm": algo_name,
            "execution_order": execution_order,
            "metrics": {
                "total_references": total_references,
                "page_hits": hits,
                "page_faults": faults,
                "hit_ratio": hit_ratio,
                "fault_ratio": fault_ratio,
                "hit_percentage": round(hit_ratio * 100, 2),
                "fault_percentage": round(fault_ratio * 100, 2),
            },
            "events": events,
            "visualization_data": {
                "final_frames": final_frames,
                "frame_capacity": self.capacity,
                "step_by_step": events
            },
            "recommendation_inputs": {
                "fault_ratio": fault_ratio,
                "hit_ratio": hit_ratio
            }
        }