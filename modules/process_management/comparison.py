from modules.process_management.scheduler import (
    FCFSScheduler, SJFScheduler, PriorityScheduler, RoundRobinScheduler
)


class SchedulerComparison:
    """
    Executes multiple scheduling algorithms on the same workload
    and compares their efficiency and execution metrics.
    """
    def __init__(self):
        self.schedulers = {
            "FCFS": FCFSScheduler(),
            "SJF (Non-Preemptive)": SJFScheduler(preemptive=False),
            "SRTF (Preemptive SJF)": SJFScheduler(preemptive=True),
            "Priority (Non-Preemptive)": PriorityScheduler(preemptive=False),
            "Priority (Preemptive)": PriorityScheduler(preemptive=True),
            "Round Robin (Q=2)": RoundRobinScheduler(time_quantum=2),
            "Round Robin (Q=4)": RoundRobinScheduler(time_quantum=4),
        }

    def add_scheduler(self, name: str, scheduler_instance):
        """Register a custom scheduler scenario for comparison."""
        self.schedulers[name] = scheduler_instance

    def compare(self, processes):
        """
        Run all registered schedulers on the input processes.
        
        Args:
            processes (list): List of original Process instances.
            
        Returns:
            dict: Mapping of scheduler name to calculated average system and process metrics.
        """
        results = {}
        for name, scheduler in self.schedulers.items():
            completed_procs, gantt_data, sys_metrics = scheduler.run(processes)
            
            if not completed_procs:
                continue
                
            total_wt = sum(p.waiting_time for p in completed_procs)
            total_tat = sum(p.turnaround_time for p in completed_procs)
            total_rt = sum(p.response_time for p in completed_procs)
            n = len(completed_procs)
            
            results[name] = {
                "avg_waiting_time": total_wt / n,
                "avg_turnaround_time": total_tat / n,
                "avg_response_time": total_rt / n,
                "throughput": sys_metrics["throughput"],
                "cpu_utilization": sys_metrics["cpu_utilization"],
                "total_time": sys_metrics["total_time"],
                "idle_time": sys_metrics["idle_time"]
            }
        return results

    def format_comparison_table(self, results) -> str:
        """Format the comparison results as a clean ASCII table."""
        headers = ["Algorithm", "Avg WT", "Avg TAT", "Avg RT", "Throughput", "CPU Util %", "Total Time"]
        lines = []
        divider = "-" * 98
        lines.append(divider)
        lines.append(
            f" {headers[0]:<28} | {headers[1]:<8} | {headers[2]:<8} | {headers[3]:<8} | {headers[4]:<10} | {headers[5]:<10} | {headers[6]:<10}"
        )
        lines.append(divider)
        for name, metrics in results.items():
            lines.append(
                f" {name:<28} | "
                f"{metrics['avg_waiting_time']:<8.2f} | "
                f"{metrics['avg_turnaround_time']:<8.2f} | "
                f"{metrics['avg_response_time']:<8.2f} | "
                f"{metrics['throughput']:<10.3f} | "
                f"{metrics['cpu_utilization']:<10.2f} | "
                f"{metrics['total_time']:<10}"
            )
        lines.append(divider)
        return "\n".join(lines)
