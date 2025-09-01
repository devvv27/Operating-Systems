class Process:
    def __init__(self, pid, arrival_time, burst_time):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.completion_time = 0
        self.waiting_time = 0
        self.turnaround_time = 0

def round_robin(processes, quantum):
    time = 0
    queue = []
    completed_processes = []

    # Sort processes by arrival time
    processes.sort(key=lambda p: p.arrival_time)

    while processes or queue:
        # Add processes that have arrived to the queue
        while processes and processes[0].arrival_time <= time:
            queue.append(processes.pop(0))

        if queue:
            current_process = queue.pop(0)
            if current_process.remaining_time > quantum:
                time += quantum
                current_process.remaining_time -= quantum
                queue.append(current_process)
            else:
                time += current_process.remaining_time
                current_process.remaining_time = 0
                current_process.completion_time = time
                current_process.turnaround_time = current_process.completion_time - current_process.arrival_time
                current_process.waiting_time = current_process.turnaround_time - current_process.burst_time
                completed_processes.append(current_process)
        else:
            time += 1

    return completed_processes

def print_processes(processes):
    print("PID\tArrival\tBurst\tCompletion\tWaiting\tTurnaround")
    for process in processes:
        print(f"{process.pid}\t{process.arrival_time}\t{process.burst_time}\t{process.completion_time}\t{process.waiting_time}\t{process.turnaround_time}")

if __name__ == "__main__":
    processes = [
        Process(1, 0, 5),
        Process(2, 1, 3),
        Process(3, 2, 8),
        Process(4, 3, 6)
    ]
    quantum = 2
    completed_processes = round_robin(processes, quantum)
    completed_processes.sort(key=lambda p: p.pid)  # Sort by PID
    print_processes(completed_processes)