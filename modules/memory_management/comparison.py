"""
Memory and Paging Comparison & Recommendation Engine
Compares contiguous allocation policies and page replacement algorithms
based on empirical metrics.
"""

from typing import List, Dict, Any
from modules.memory_management.allocator import MemoryAllocator
from modules.memory_management.paging import PageReplacementManager


class MemoryComparisonEngine:
    """
    Compares Contiguous Memory Allocation algorithms:
    - First Fit
    - Best Fit
    - Worst Fit
    - Next Fit
    """
    @staticmethod
    def compare_allocators(
        partition_sizes: List[int],
        requests: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        algorithms = ["First Fit", "Best Fit", "Worst Fit", "Next Fit"]
        results = {}

        for algo in algorithms:
            allocator = MemoryAllocator(partition_sizes)
            results[algo] = allocator.run_simulation(algo, requests)

        comparison_table = []
        best_algo = None
        min_internal_frag = float("inf")
        max_allocated = -1

        for algo, res in results.items():
            metrics = res["metrics"]
            allocated_count = metrics["allocated_blocks_count"]
            internal_frag = metrics["internal_fragmentation"]
            utilization = metrics["utilization_percentage"]

            row = {
                "algorithm": algo,
                "allocated_processes": allocated_count,
                "unallocated_processes": len(requests) - allocated_count,
                "utilization_percentage": utilization,
                "internal_fragmentation": internal_frag,
            }
            comparison_table.append(row)

            # Recommendation heuristic: prioritize successful allocations, then lowest internal fragmentation
            if (allocated_count > max_allocated) or (
                allocated_count == max_allocated and internal_frag < min_internal_frag
            ):
                max_allocated = allocated_count
                min_internal_frag = internal_frag
                best_algo = algo

        recommendation = (
            f"'{best_algo}' is recommended for this workload because it successfully allocated "
            f"{max_allocated}/{len(requests)} processes while maintaining an internal fragmentation of "
            f"{min_internal_frag} units."
        )

        return {
            "status": "success",
            "type": "Contiguous Allocation Comparison",
            "comparison_table": comparison_table,
            "individual_results": results,
            "recommendation": {
                "recommended_algorithm": best_algo,
                "rationale": recommendation
            }
        }


class PagingComparisonEngine:
    """
    Compares Page Replacement algorithms:
    - FIFO
    - LRU
    """
    @staticmethod
    def compare_paging(
        capacity: int,
        reference_string: List[int]
    ) -> Dict[str, Any]:
        manager = PageReplacementManager(capacity=capacity)
        fifo_result = manager.run_fifo(reference_string)
        lru_result = manager.run_lru(reference_string)

        fifo_faults = fifo_result["metrics"]["page_faults"]
        lru_faults = lru_result["metrics"]["page_faults"]

        comparison_table = [
            {
                "algorithm": "FIFO",
                "page_hits": fifo_result["metrics"]["page_hits"],
                "page_faults": fifo_faults,
                "hit_percentage": fifo_result["metrics"]["hit_percentage"],
                "fault_percentage": fifo_result["metrics"]["fault_percentage"],
            },
            {
                "algorithm": "LRU",
                "page_hits": lru_result["metrics"]["page_hits"],
                "page_faults": lru_faults,
                "hit_percentage": lru_result["metrics"]["hit_percentage"],
                "fault_percentage": lru_result["metrics"]["fault_percentage"],
            }
        ]

        if lru_faults < fifo_faults:
            best_algo = "LRU"
            rationale = (
                f"LRU produced fewer page faults ({lru_faults}) compared to FIFO ({fifo_faults}), "
                f"effectively leveraging temporal locality."
            )
        elif fifo_faults < lru_faults:
            best_algo = "FIFO"
            rationale = (
                f"FIFO produced fewer page faults ({fifo_faults}) compared to LRU ({lru_faults}) "
                f"on this specific reference sequence."
            )
        else:
            best_algo = "LRU / FIFO (Tied)"
            rationale = f"Both algorithms resulted in identical page fault counts ({lru_faults})."

        return {
            "status": "success",
            "type": "Page Replacement Comparison",
            "comparison_table": comparison_table,
            "results": {
                "FIFO": fifo_result,
                "LRU": lru_result
            },
            "recommendation": {
                "recommended_algorithm": best_algo,
                "rationale": rationale
            }
        }