from core.data_structure.queue.queue import Queue
from core.data_structure.priority_queue.priority_queue import PriorityQueue
from modules.process_management.process import Process, ProcessState
from modules.process_management.gantt import GanttChart
from modules.process_management.metrics import SchedulerMetrics


class BaseScheduler:
    """Base class for all scheduling algorithms."""
    def __init__(self):
        self.gantt_chart = GanttChart()
        self.total_time = 0
        self.idle_time = 0
        self.processes = []

    def run(self, processes):
        """
        Execute the scheduling algorithm. Must be overridden by subclasses.
        Returns:
            tuple: (processes with computed metrics, gantt chart data, system metrics dict)
        """
        raise NotImplementedError("Subclasses must implement run method")

    def _prepare_processes(self, processes):
        """Create a deep copy of processes and reset them for the simulation."""
        self.processes = [
            Process(p.pid, p.arrival_time, p.burst_time, p.priority)
            for p in processes
        ]
        # Sort initially by arrival time to facilitate arrival queue management
        self.processes.sort(key=lambda p: (p.arrival_time, p.pid))
        self.gantt_chart.reset()
        self.total_time = 0
        self.idle_time = 0
        return self.processes


class FCFSScheduler(BaseScheduler):
    """
    First-Come, First-Served (FCFS) Scheduling Algorithm (Non-preemptive).
    
    Time Complexity: O(N log N) for initial sort, O(N) for simulation.
    Space Complexity: O(N) for ready queue.
    """
    def run(self, processes):
        procs = self._prepare_processes(processes)
        if not procs:
            return [], [], SchedulerMetrics.calculate_system_metrics([], 0, 0)

        ready_queue = Queue()
        current_time = 0
        arrival_idx = 0
        n = len(procs)
        completed = 0
        running_proc = None

        while completed < n:
            # Enqueue all processes that have arrived by the current time
            while arrival_idx < n and procs[arrival_idx].arrival_time <= current_time:
                ready_queue.enqueue(procs[arrival_idx])
                arrival_idx += 1

            if running_proc is None:
                if not ready_queue.is_empty():
                    running_proc = ready_queue.dequeue()
                    running_proc.state = ProcessState.RUNNING
                    if running_proc.start_time == -1:
                        running_proc.start_time = current_time
                        running_proc.response_time = current_time - running_proc.arrival_time
                else:
                    # CPU is idle
                    self.gantt_chart.add_entry(current_time, current_time + 1, "IDLE")
                    self.idle_time += 1
                    current_time += 1
                    continue

            # Execute running process
            self.gantt_chart.add_entry(current_time, current_time + 1, running_proc.pid)
            running_proc.remaining_time -= 1
            current_time += 1

            if running_proc.remaining_time == 0:
                running_proc.completion_time = current_time
                running_proc.state = ProcessState.TERMINATED
                completed += 1
                running_proc = None

        self.total_time = current_time
        SchedulerMetrics.calculate_process_metrics(procs)
        sys_metrics = SchedulerMetrics.calculate_system_metrics(procs, self.total_time, self.idle_time)
        return procs, self.gantt_chart.get_data(), sys_metrics


class SJFScheduler(BaseScheduler):
    """
    Shortest Job First (SJF) Scheduling Algorithm.
    Supports both Non-preemptive (SJF) and Preemptive (Shortest Remaining Time First - SRTF).
    
    Time Complexity: O(N log N) due to Heap/PriorityQueue insertions/deletions.
    Space Complexity: O(N) for ready queue.
    """
    def __init__(self, preemptive: bool = False):
        super().__init__()
        self.preemptive = preemptive

    def run(self, processes):
        procs = self._prepare_processes(processes)
        if not procs:
            return [], [], SchedulerMetrics.calculate_system_metrics([], 0, 0)

        # Non-preemptive sorts by original burst_time
        # Preemptive sorts by remaining_time
        key_fn = (lambda p: (p.remaining_time, p.arrival_time, p.pid)) if self.preemptive \
            else (lambda p: (p.burst_time, p.arrival_time, p.pid))
        
        ready_queue = PriorityQueue(key=key_fn, is_min_heap=True)
        current_time = 0
        arrival_idx = 0
        n = len(procs)
        completed = 0
        running_proc = None

        while completed < n:
            # Enqueue all processes that have arrived by current time
            while arrival_idx < n and procs[arrival_idx].arrival_time <= current_time:
                ready_queue.enqueue(procs[arrival_idx])
                arrival_idx += 1

            if self.preemptive and running_proc is not None:
                # Check for preemption if a shorter job arrived
                if not ready_queue.is_empty():
                    shortest_waiting = ready_queue.peek()
                    if shortest_waiting.remaining_time < running_proc.remaining_time:
                        running_proc.state = ProcessState.READY
                        ready_queue.enqueue(running_proc)
                        running_proc = None

            if running_proc is None:
                if not ready_queue.is_empty():
                    running_proc = ready_queue.dequeue()
                    running_proc.state = ProcessState.RUNNING
                    if running_proc.start_time == -1:
                        running_proc.start_time = current_time
                        running_proc.response_time = current_time - running_proc.arrival_time
                else:
                    self.gantt_chart.add_entry(current_time, current_time + 1, "IDLE")
                    self.idle_time += 1
                    current_time += 1
                    continue

            # Execute running process
            self.gantt_chart.add_entry(current_time, current_time + 1, running_proc.pid)
            running_proc.remaining_time -= 1
            current_time += 1

            if running_proc.remaining_time == 0:
                running_proc.completion_time = current_time
                running_proc.state = ProcessState.TERMINATED
                completed += 1
                running_proc = None

        self.total_time = current_time
        SchedulerMetrics.calculate_process_metrics(procs)
        sys_metrics = SchedulerMetrics.calculate_system_metrics(procs, self.total_time, self.idle_time)
        return procs, self.gantt_chart.get_data(), sys_metrics


class PriorityScheduler(BaseScheduler):
    """
    Priority Scheduling Algorithm.
    Supports both Non-preemptive and Preemptive priority scheduling.
    Configurable priority ordering (default: lower integer = higher priority).
    
    Time Complexity: O(N log N) due to Heap/PriorityQueue.
    Space Complexity: O(N) for ready queue.
    """
    def __init__(self, preemptive: bool = False, lower_is_higher_priority: bool = True):
        super().__init__()
        self.preemptive = preemptive
        self.lower_is_higher_priority = lower_is_higher_priority

    def run(self, processes):
        procs = self._prepare_processes(processes)
        if not procs:
            return [], [], SchedulerMetrics.calculate_system_metrics([], 0, 0)

        # Key extractor mapping priority. If lower is higher priority, we use standard values.
        # Otherwise we negate the values to implement a min-heap behaving as a max-heap.
        if self.lower_is_higher_priority:
            key_fn = lambda p: (p.priority, p.arrival_time, p.pid)
        else:
            key_fn = lambda p: (-p.priority, p.arrival_time, p.pid)

        ready_queue = PriorityQueue(key=key_fn, is_min_heap=True)
        current_time = 0
        arrival_idx = 0
        n = len(procs)
        completed = 0
        running_proc = None

        while completed < n:
            # Enqueue all processes that have arrived by current time
            while arrival_idx < n and procs[arrival_idx].arrival_time <= current_time:
                ready_queue.enqueue(procs[arrival_idx])
                arrival_idx += 1

            if self.preemptive and running_proc is not None:
                # Check for preemption if a higher priority job arrived
                if not ready_queue.is_empty():
                    highest_priority_waiting = ready_queue.peek()
                    # If lower is higher, look for smaller priority value
                    # If higher is higher, we negated the values, so smaller is still correct
                    running_key = -running_proc.priority if not self.lower_is_higher_priority else running_proc.priority
                    waiting_key = -highest_priority_waiting.priority if not self.lower_is_higher_priority else highest_priority_waiting.priority
                    if waiting_key < running_key:
                        running_proc.state = ProcessState.READY
                        ready_queue.enqueue(running_proc)
                        running_proc = None

            if running_proc is None:
                if not ready_queue.is_empty():
                    running_proc = ready_queue.dequeue()
                    running_proc.state = ProcessState.RUNNING
                    if running_proc.start_time == -1:
                        running_proc.start_time = current_time
                        running_proc.response_time = current_time - running_proc.arrival_time
                else:
                    self.gantt_chart.add_entry(current_time, current_time + 1, "IDLE")
                    self.idle_time += 1
                    current_time += 1
                    continue

            # Execute running process
            self.gantt_chart.add_entry(current_time, current_time + 1, running_proc.pid)
            running_proc.remaining_time -= 1
            current_time += 1

            if running_proc.remaining_time == 0:
                running_proc.completion_time = current_time
                running_proc.state = ProcessState.TERMINATED
                completed += 1
                running_proc = None

        self.total_time = current_time
        SchedulerMetrics.calculate_process_metrics(procs)
        sys_metrics = SchedulerMetrics.calculate_system_metrics(procs, self.total_time, self.idle_time)
        return procs, self.gantt_chart.get_data(), sys_metrics


class RoundRobinScheduler(BaseScheduler):
    """
    Round Robin (RR) Scheduling Algorithm (Preemptive by Time Quantum).
    
    Time Complexity: O(N) simulation operations, O(N) space.
    """
    def __init__(self, time_quantum: int = 2):
        super().__init__()
        if time_quantum <= 0:
            raise ValueError("Time quantum must be greater than 0")
        self.time_quantum = time_quantum

    def run(self, processes):
        procs = self._prepare_processes(processes)
        if not procs:
            return [], [], SchedulerMetrics.calculate_system_metrics([], 0, 0)

        ready_queue = Queue()
        current_time = 0
        arrival_idx = 0
        n = len(procs)
        completed = 0
        running_proc = None
        quantum_spent = 0

        while completed < n:
            # Enqueue all processes that have arrived by current time
            # Important: newly arrived processes are enqueued first
            while arrival_idx < n and procs[arrival_idx].arrival_time <= current_time:
                ready_queue.enqueue(procs[arrival_idx])
                arrival_idx += 1

            if running_proc is None:
                if not ready_queue.is_empty():
                    running_proc = ready_queue.dequeue()
                    running_proc.state = ProcessState.RUNNING
                    quantum_spent = 0
                    if running_proc.start_time == -1:
                        running_proc.start_time = current_time
                        running_proc.response_time = current_time - running_proc.arrival_time
                else:
                    self.gantt_chart.add_entry(current_time, current_time + 1, "IDLE")
                    self.idle_time += 1
                    current_time += 1
                    continue

            # Execute running process
            self.gantt_chart.add_entry(current_time, current_time + 1, running_proc.pid)
            running_proc.remaining_time -= 1
            quantum_spent += 1
            current_time += 1

            # Check if finished
            if running_proc.remaining_time == 0:
                running_proc.completion_time = current_time
                running_proc.state = ProcessState.TERMINATED
                completed += 1
                running_proc = None
            # Check if time quantum expired
            elif quantum_spent == self.time_quantum:
                # Enqueue newly arrived processes first before re-queuing the preempted one
                while arrival_idx < n and procs[arrival_idx].arrival_time <= current_time:
                    ready_queue.enqueue(procs[arrival_idx])
                    arrival_idx += 1
                
                running_proc.state = ProcessState.READY
                ready_queue.enqueue(running_proc)
                running_proc = None

        self.total_time = current_time
        SchedulerMetrics.calculate_process_metrics(procs)
        sys_metrics = SchedulerMetrics.calculate_system_metrics(procs, self.total_time, self.idle_time)
        return procs, self.gantt_chart.get_data(), sys_metrics
