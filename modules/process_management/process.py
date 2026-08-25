class ProcessState:
    READY = "READY"
    RUNNING = "RUNNING"
    WAITING = "WAITING"
    TERMINATED = "TERMINATED"


class Process:
    """
    Represents a Process in the Operating System scheduling simulation.
    Tracks state transitions and timing metrics.
    """
    def __init__(self, pid: int, arrival_time: int, burst_time: int, priority: int = 0):
        """
        Initialize the process.
        
        Args:
            pid (int): Unique process identifier.
            arrival_time (int): The simulation time at which process arrives in ready queue.
            burst_time (int): CPU execution time required.
            priority (int, optional): Process priority (lower/higher value logic depends on scheduling config).
        """
        if arrival_time < 0:
            raise ValueError(f"Process PID {pid}: arrival_time cannot be negative (got {arrival_time})")
        if burst_time <= 0:
            raise ValueError(f"Process PID {pid}: burst_time must be greater than 0 (got {burst_time})")

        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority
        self.state = ProcessState.READY
        
        # Timing metrics
        self.remaining_time = burst_time
        self.completion_time = 0
        self.waiting_time = 0
        self.turnaround_time = 0
        self.response_time = -1  # -1 represents not yet started
        
        # Internal tracker to log when the process first starts running
        self.start_time = -1

    def reset(self):
        """Reset the execution state for reuse in different scheduling runs."""
        self.state = ProcessState.READY
        self.remaining_time = self.burst_time
        self.completion_time = 0
        self.waiting_time = 0
        self.turnaround_time = 0
        self.response_time = -1
        self.start_time = -1

    def __repr__(self):
        return (f"Process(PID={self.pid}, Arrival={self.arrival_time}, Burst={self.burst_time}, "
                f"Priority={self.priority}, State={self.state}, Remaining={self.remaining_time})")
