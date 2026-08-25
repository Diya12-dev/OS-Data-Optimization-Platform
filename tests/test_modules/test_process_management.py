import unittest
import sys
import os

# Adjust path to import modules properly
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from modules.process_management.process import Process
from modules.process_management.scheduler import (
    FCFSScheduler, SJFScheduler, PriorityScheduler, RoundRobinScheduler
)
from modules.process_management.comparison import SchedulerComparison


class TestProcessScheduling(unittest.TestCase):
    def setUp(self):
        # Sample processes: (PID, Arrival Time, Burst Time, Priority)
        self.workload = [
            Process(pid=1, arrival_time=0, burst_time=8, priority=3),
            Process(pid=2, arrival_time=1, burst_time=4, priority=1),
            Process(pid=3, arrival_time=2, burst_time=9, priority=4),
            Process(pid=4, arrival_time=3, burst_time=5, priority=2)
        ]

    def test_process_validation_negative_arrival(self):
        with self.assertRaises(ValueError):
            Process(pid=9, arrival_time=-1, burst_time=5)

    def test_process_validation_invalid_burst(self):
        with self.assertRaises(ValueError):
            Process(pid=9, arrival_time=0, burst_time=0)
        with self.assertRaises(ValueError):
            Process(pid=9, arrival_time=0, burst_time=-3)

    def test_fcfs_scheduling(self):
        scheduler = FCFSScheduler()
        completed_procs, gantt_data, sys_metrics = scheduler.run(self.workload)

        # FCFS processes should execute in order of arrival: 1, 2, 3, 4
        # PID 1: Arrives at 0, Runs 0-8. CT=8, TAT=8, WT=0
        # PID 2: Arrives at 1, Runs 8-12. CT=12, TAT=11, WT=7
        # PID 3: Arrives at 2, Runs 12-21. CT=21, TAT=19, WT=10
        # PID 4: Arrives at 3, Runs 21-26. CT=26, TAT=23, WT=18
        
        proc_map = {p.pid: p for p in completed_procs}
        
        self.assertEqual(proc_map[1].completion_time, 8)
        self.assertEqual(proc_map[1].waiting_time, 0)
        self.assertEqual(proc_map[1].turnaround_time, 8)

        self.assertEqual(proc_map[2].completion_time, 12)
        self.assertEqual(proc_map[2].waiting_time, 7)
        self.assertEqual(proc_map[2].turnaround_time, 11)

        self.assertEqual(proc_map[3].completion_time, 21)
        self.assertEqual(proc_map[3].waiting_time, 10)
        self.assertEqual(proc_map[3].turnaround_time, 19)

        self.assertEqual(proc_map[4].completion_time, 26)
        self.assertEqual(proc_map[4].waiting_time, 18)
        self.assertEqual(proc_map[4].turnaround_time, 23)

        self.assertEqual(sys_metrics["total_time"], 26)
        self.assertEqual(sys_metrics["idle_time"], 0)
        self.assertEqual(len(gantt_data), 4)

    def test_sjf_non_preemptive(self):
        scheduler = SJFScheduler(preemptive=False)
        completed_procs, gantt_data, sys_metrics = scheduler.run(self.workload)

        # SJF Non-preemptive:
        # P1 starts at 0, runs to 8 (since no other process is in the queue at t=0).
        # At t=8: P2(burst 4), P4(burst 5), P3(burst 9) are in the queue.
        # SJF runs P2 (8 to 12).
        # At t=12: P4(burst 5), P3(burst 9) remain. Runs P4 (12 to 17).
        # At t=17: Runs P3 (17 to 26).
        proc_map = {p.pid: p for p in completed_procs}

        self.assertEqual(proc_map[1].completion_time, 8)
        self.assertEqual(proc_map[2].completion_time, 12)
        self.assertEqual(proc_map[4].completion_time, 17)
        self.assertEqual(proc_map[3].completion_time, 26)

    def test_sjf_preemptive_srtf(self):
        scheduler = SJFScheduler(preemptive=True)
        completed_procs, gantt_data, sys_metrics = scheduler.run(self.workload)

        # SRTF:
        # P1 starts at 0.
        # At t=1: P2(burst 4) arrives. P1's remaining is 7. P2 preempts P1.
        # P2 runs t=1 to 5. (P3 arrives at 2, P4 arrives at 3).
        # At t=5: P2 finishes. Ready queue: P4(burst 5), P1(remaining 7), P3(burst 9).
        # SRTF runs P4 (5 to 10).
        # At t=10: P4 finishes. Ready queue: P1(remaining 7), P3(burst 9). Runs P1 (10 to 17).
        # At t=17: P1 finishes. Runs P3 (17 to 26).
        proc_map = {p.pid: p for p in completed_procs}

        self.assertEqual(proc_map[2].completion_time, 5)
        self.assertEqual(proc_map[4].completion_time, 10)
        self.assertEqual(proc_map[1].completion_time, 17)
        self.assertEqual(proc_map[3].completion_time, 26)

    def test_priority_non_preemptive(self):
        # Low values represent high priorities: 1 (highest), 2, 3, 4 (lowest)
        scheduler = PriorityScheduler(preemptive=False, lower_is_higher_priority=True)
        completed_procs, gantt_data, sys_metrics = scheduler.run(self.workload)

        # P1 starts at 0, runs to 8.
        # At t=8: Queue has P2(priority 1), P4(priority 2), P3(priority 4).
        # Runs P2 (8 to 12).
        # Runs P4 (12 to 17).
        # Runs P3 (17 to 26).
        proc_map = {p.pid: p for p in completed_procs}

        self.assertEqual(proc_map[1].completion_time, 8)
        self.assertEqual(proc_map[2].completion_time, 12)
        self.assertEqual(proc_map[4].completion_time, 17)
        self.assertEqual(proc_map[3].completion_time, 26)

    def test_priority_preemptive(self):
        scheduler = PriorityScheduler(preemptive=True, lower_is_higher_priority=True)
        completed_procs, gantt_data, sys_metrics = scheduler.run(self.workload)

        # P1 (priority 3) starts at 0.
        # At t=1: P2 (priority 1) arrives and preempts P1.
        # P2 runs 1 to 5.
        # At t=5: Ready queue: P4 (priority 2), P1 (priority 3), P3 (priority 4).
        # Runs P4 (5 to 10).
        # Runs P1 (10 to 17).
        # Runs P3 (17 to 26).
        proc_map = {p.pid: p for p in completed_procs}

        self.assertEqual(proc_map[2].completion_time, 5)
        self.assertEqual(proc_map[4].completion_time, 10)
        self.assertEqual(proc_map[1].completion_time, 17)
        self.assertEqual(proc_map[3].completion_time, 26)

    def test_round_robin(self):
        # Time Quantum = 2
        # P1: arr=0, burst=8 (req 4 slots of size 2)
        # P2: arr=1, burst=4 (req 2 slots of size 2)
        # P3: arr=2, burst=9 (req 5 slots: 2, 2, 2, 2, 1)
        # P4: arr=3, burst=5 (req 3 slots: 2, 2, 1)
        scheduler = RoundRobinScheduler(time_quantum=2)
        completed_procs, gantt_data, sys_metrics = scheduler.run(self.workload)
        
        proc_map = {p.pid: p for p in completed_procs}
        
        # Checking if total time is exactly sum of burst times (26) and working tree clean
        self.assertEqual(sys_metrics["total_time"], 26)
        self.assertTrue(all(p.state == "TERMINATED" for p in completed_procs))

    def test_comparison_runner(self):
        comparison = SchedulerComparison()
        results = comparison.compare(self.workload)
        self.assertIn("FCFS", results)
        self.assertIn("SRTF (Preemptive SJF)", results)
        self.assertIn("Round Robin (Q=2)", results)

        table_str = comparison.format_comparison_table(results)
        self.assertTrue(len(table_str) > 0)
        # Verify it prints correctly
        print("\n" + table_str)


if __name__ == '__main__':
    unittest.main()
