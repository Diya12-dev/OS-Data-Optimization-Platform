class GanttChartEntry:
    """Represents a single continuous interval of CPU execution."""
    def __init__(self, start_time: int, end_time: int, pid: int or str):
        self.start_time = start_time
        self.end_time = end_time
        self.pid = pid  # PID integer, or "IDLE"

    def to_dict(self):
        return {
            "start_time": self.start_time,
            "end_time": self.end_time,
            "pid": self.pid
        }

    def __repr__(self):
        return f"[{self.start_time}-{self.end_time}: PID {self.pid}]"


class GanttChart:
    """Manages the chronology of scheduled CPU intervals."""
    def __init__(self):
        self.entries = []

    def add_entry(self, start_time: int, end_time: int, pid: int or str):
        """
        Record a scheduled time slot. Merges consecutive slots of the same process.
        """
        if start_time >= end_time:
            return
        
        # Merge if consecutive running CPU burst is for the same process
        if self.entries and self.entries[-1].pid == pid and self.entries[-1].end_time == start_time:
            self.entries[-1].end_time = end_time
        else:
            self.entries.append(GanttChartEntry(start_time, end_time, pid))

    def get_data(self):
        """Return raw format of Gantt chart entries for visualization layer."""
        return [entry.to_dict() for entry in self.entries]

    def reset(self):
        """Clear all entries."""
        self.entries = []
