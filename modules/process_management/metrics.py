class SchedulerMetrics:
    """Provides methods for calculating scheduler and process timing metrics."""
    
    @staticmethod
    def calculate_process_metrics(processes):
        """
        Calculate waiting time and turnaround time for each process.
        Assumes arrival_time, burst_time, completion_time, and response_time are set.
        
        Time Complexity: O(N) where N is number of processes.
        Space Complexity: O(1)
        """
        for p in processes:
            p.turnaround_time = p.completion_time - p.arrival_time
            p.waiting_time = p.turnaround_time - p.burst_time
            # response_time is set dynamically during simulation when the process first executes

    @staticmethod
    def calculate_system_metrics(processes, total_time: int, idle_time: int):
        """
        Calculate scheduling algorithm efficiency metrics: Throughput and CPU Utilization.
        
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        if total_time <= 0:
            return {
                "throughput": 0.0,
                "cpu_utilization": 0.0,
                "total_time": 0,
                "idle_time": 0
            }
        
        num_processes = len(processes)
        throughput = num_processes / total_time
        cpu_utilization = ((total_time - idle_time) / total_time) * 100.0
        
        return {
            "throughput": throughput,
            "cpu_utilization": cpu_utilization,
            "total_time": total_time,
            "idle_time": idle_time
        }
