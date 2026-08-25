import unittest

from modules.process_management.process import Process, ProcessState
from modules.process_management.scheduler import (
    FCFSScheduler,
    SJFScheduler,
    PriorityScheduler,
    RoundRobinScheduler,
)
from modules.process_management.comparison import SchedulerComparison


class TestProcessManagerIntegration(unittest.TestCase):

    def setUp(self):
        self.workload = [
            Process(pid=1, arrival_time=0, burst_time=5, priority=2),
            Process(pid=2, arrival_time=1, burst_time=3, priority=1),
            Process(pid=3, arrival_time=2, burst_time=4, priority=3),
        ]

    def test_all_schedulers_produce_valid_output(self):
        schedulers = [
            FCFSScheduler(),
            SJFScheduler(preemptive=False),
            SJFScheduler(preemptive=True),
            PriorityScheduler(preemptive=False),
            PriorityScheduler(preemptive=True),
            RoundRobinScheduler(time_quantum=2),
        ]

        for scheduler in schedulers:
            with self.subTest(scheduler=scheduler.__class__.__name__):
                completed, gantt, metrics = scheduler.run(self.workload)

                self.assertEqual(len(completed), len(self.workload))
                self.assertTrue(
                    all(p.state == ProcessState.TERMINATED for p in completed)
                )
                self.assertTrue(len(gantt) > 0)

                self.assertIn("throughput", metrics)
                self.assertIn("cpu_utilization", metrics)
                self.assertIn("total_time", metrics)
                self.assertIn("idle_time", metrics)

    def test_original_processes_are_not_modified(self):
        original = [
            Process(pid=1, arrival_time=0, burst_time=5, priority=2),
            Process(pid=2, arrival_time=1, burst_time=3, priority=1),
        ]

        original_values = [
            (p.pid, p.arrival_time, p.burst_time, p.priority)
            for p in original
        ]

        FCFSScheduler().run(original)

        after_values = [
            (p.pid, p.arrival_time, p.burst_time, p.priority)
            for p in original
        ]

        self.assertEqual(original_values, after_values)

        for process in original:
            self.assertEqual(process.remaining_time, process.burst_time)
            self.assertEqual(process.state, ProcessState.READY)

    def test_same_workload_can_be_compared_multiple_times(self):
        comparison = SchedulerComparison()

        first_result = comparison.compare(self.workload)
        second_result = comparison.compare(self.workload)

        self.assertEqual(set(first_result.keys()), set(second_result.keys()))

        for algorithm in first_result:
            self.assertEqual(
                first_result[algorithm],
                second_result[algorithm]
            )

    def test_empty_workload(self):
        schedulers = [
            FCFSScheduler(),
            SJFScheduler(),
            PriorityScheduler(),
            RoundRobinScheduler(time_quantum=2),
        ]

        for scheduler in schedulers:
            with self.subTest(scheduler=scheduler.__class__.__name__):
                completed, gantt, metrics = scheduler.run([])

                self.assertEqual(completed, [])
                self.assertEqual(gantt, [])
                self.assertEqual(metrics["total_time"], 0)
                self.assertEqual(metrics["idle_time"], 0)

    def test_idle_cpu_is_recorded(self):
        workload = [
            Process(pid=1, arrival_time=3, burst_time=2, priority=1),
        ]

        completed, gantt, metrics = FCFSScheduler().run(workload)

        self.assertEqual(metrics["idle_time"], 3)
        self.assertEqual(metrics["total_time"], 5)

        self.assertEqual(gantt[0]["pid"], "IDLE")
        self.assertEqual(gantt[0]["start_time"], 0)
        self.assertEqual(gantt[0]["end_time"], 3)

        self.assertEqual(completed[0].completion_time, 5)


if __name__ == "__main__":
    unittest.main()