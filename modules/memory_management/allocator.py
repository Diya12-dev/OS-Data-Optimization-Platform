"""
Memory Allocator Module
Implements Contiguous Memory Allocation strategies:
- First Fit
- Best Fit
- Worst Fit
- Next Fit
Calculates memory utilization, internal fragmentation, and external fragmentation.
"""

from typing import List, Dict, Any, Optional
from core.data_structure.bitmap.bitmap import Bitmap


class MemoryBlock:
    """Represents a continuous segment of physical memory."""
    def __init__(self, block_id: int, start: int, size: int):
        self.block_id = block_id
        self.start = start
        self.size = size
        self.is_allocated = False
        self.process_id: Optional[str] = None
        self.allocated_size: int = 0  # Actual memory used by process

    @property
    def internal_fragmentation(self) -> int:
        if self.is_allocated and self.allocated_size > 0:
            return max(0, self.size - self.allocated_size)
        return 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "block_id": self.block_id,
            "start": self.start,
            "size": self.size,
            "is_allocated": self.is_allocated,
            "process_id": self.process_id,
            "allocated_size": self.allocated_size,
            "internal_fragmentation": self.internal_fragmentation,
        }


class MemoryAllocator:
    """
    Contiguous Memory Allocation Manager.
    Supports First Fit, Best Fit, Worst Fit, and Next Fit.
    """
    def __init__(self, partition_sizes: List[int]):
        if not partition_sizes or any(s <= 0 for s in partition_sizes):
            raise ValueError("Partition sizes must be non-empty and all values > 0.")

        self.partition_sizes = list(partition_sizes)
        self.total_memory = sum(partition_sizes)
        self.bitmap = Bitmap(self.total_memory)
        self.blocks: List[MemoryBlock] = []
        self.last_allocated_index = 0  # For Next Fit

        current_offset = 0
        for i, size in enumerate(partition_sizes):
            self.blocks.append(MemoryBlock(block_id=i, start=current_offset, size=size))
            current_offset += size

    def reset(self) -> None:
        """Reset all partitions to free state."""
        self.bitmap = Bitmap(self.total_memory)
        self.last_allocated_index = 0
        current_offset = 0
        self.blocks = []
        for i, size in enumerate(self.partition_sizes):
            self.blocks.append(MemoryBlock(block_id=i, start=current_offset, size=size))
            current_offset += size

    def _find_free_blocks(self) -> List[int]:
        """Return list of indices of unallocated blocks."""
        return [i for i, b in enumerate(self.blocks) if not b.is_allocated]

    def allocate_first_fit(self, process_id: str, requested_size: int) -> Optional[int]:
        """First Fit: Allocate the first free block that fits."""
        for i, block in enumerate(self.blocks):
            if not block.is_allocated and block.size >= requested_size:
                self._assign_block(i, process_id, requested_size)
                return i
        return None

    def allocate_best_fit(self, process_id: str, requested_size: int) -> Optional[int]:
        """Best Fit: Allocate the smallest free block that fits."""
        best_idx = None
        min_waste = float("inf")

        for i, block in enumerate(self.blocks):
            if not block.is_allocated and block.size >= requested_size:
                waste = block.size - requested_size
                if waste < min_waste:
                    min_waste = waste
                    best_idx = i

        if best_idx is not None:
            self._assign_block(best_idx, process_id, requested_size)
            return best_idx
        return None

    def allocate_worst_fit(self, process_id: str, requested_size: int) -> Optional[int]:
        """Worst Fit: Allocate the largest free block that fits."""
        worst_idx = None
        max_waste = -1

        for i, block in enumerate(self.blocks):
            if not block.is_allocated and block.size >= requested_size:
                waste = block.size - requested_size
                if waste > max_waste:
                    max_waste = waste
                    worst_idx = i

        if worst_idx is not None:
            self._assign_block(worst_idx, process_id, requested_size)
            return worst_idx
        return None

    def allocate_next_fit(self, process_id: str, requested_size: int) -> Optional[int]:
        """Next Fit: Like First Fit, but starts search from the last allocated index."""
        num_blocks = len(self.blocks)
        for offset in range(num_blocks):
            idx = (self.last_allocated_index + offset) % num_blocks
            block = self.blocks[idx]
            if not block.is_allocated and block.size >= requested_size:
                self._assign_block(idx, process_id, requested_size)
                self.last_allocated_index = idx
                return idx
        return None

    def deallocate(self, block_id: int) -> bool:
        """Release an allocated block back to free state."""
        if block_id < 0 or block_id >= len(self.blocks):
            return False
        block = self.blocks[block_id]
        if not block.is_allocated:
            return False

        self.bitmap.free_range(block.start, block.allocated_size)
        block.is_allocated = False
        block.process_id = None
        block.allocated_size = 0
        return True

    def _assign_block(self, block_idx: int, process_id: str, size: int) -> None:
        block = self.blocks[block_idx]
        block.is_allocated = True
        block.process_id = process_id
        block.allocated_size = size
        self.bitmap.allocate_range(block.start, size)

    # --- Metrics Calculations ---
    def get_metrics(self, pending_request_size: int = 0) -> Dict[str, Any]:
        """
        Calculate Memory Utilization, Internal Fragmentation, and External Fragmentation.
        """
        allocated_bytes = sum(b.allocated_size for b in self.blocks if b.is_allocated)
        total_internal_frag = sum(b.internal_fragmentation for b in self.blocks if b.is_allocated)
        free_blocks = [b for b in self.blocks if not b.is_allocated]
        total_free_space = sum(b.size for b in free_blocks)

        # External fragmentation occurs when total free space is sufficient for a request,
        # but no single continuous block is large enough.
        max_contiguous_free = max((b.size for b in free_blocks), default=0)
        has_external_frag = (
            pending_request_size > 0
            and total_free_space >= pending_request_size
            and max_contiguous_free < pending_request_size
        )

        utilization_pct = (allocated_bytes / self.total_memory * 100.0) if self.total_memory > 0 else 0.0

        return {
            "total_memory": self.total_memory,
            "allocated_memory": allocated_bytes,
            "free_memory": total_free_space,
            "utilization_percentage": round(utilization_pct, 2),
            "internal_fragmentation": total_internal_frag,
            "external_fragmentation_detected": has_external_frag,
            "total_external_fragmentation_space": total_free_space if has_external_frag else 0,
            "free_blocks_count": len(free_blocks),
            "allocated_blocks_count": len(self.blocks) - len(free_blocks),
        }

    # --- Standard Result Format ---
    def run_simulation(self, algorithm: str, requests: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Execute batch requests with the chosen algorithm and return standard result format.
        Each request is dict: {"process_id": "P1", "size": 100}
        """
        self.reset()
        algo_func = {
            "First Fit": self.allocate_first_fit,
            "Best Fit": self.allocate_best_fit,
            "Worst Fit": self.allocate_worst_fit,
            "Next Fit": self.allocate_next_fit,
        }.get(algorithm)

        if not algo_func:
            raise ValueError(f"Unknown algorithm '{algorithm}'. Choose First Fit, Best Fit, Worst Fit, or Next Fit.")

        events = []
        execution_order = []

        for req in requests:
            pid = req["process_id"]
            size = req["size"]
            allocated_idx = algo_func(pid, size)
            
            if allocated_idx is not None:
                execution_order.append(pid)
                events.append({
                    "process_id": pid,
                    "requested_size": size,
                    "allocated_block": allocated_idx,
                    "status": "allocated"
                })
            else:
                events.append({
                    "process_id": pid,
                    "requested_size": size,
                    "allocated_block": None,
                    "status": "failed"
                })

        return {
            "status": "success",
            "algorithm": algorithm,
            "execution_order": execution_order,
            "metrics": self.get_metrics(),
            "events": events,
            "visualization_data": {
                "blocks": [b.to_dict() for b in self.blocks],
                "bitmap": self.bitmap.to_list(),
            },
            "recommendation_inputs": {
                "utilization": self.get_metrics()["utilization_percentage"],
                "internal_fragmentation": self.get_metrics()["internal_fragmentation"],
            }
        }