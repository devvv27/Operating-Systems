class Process:
    def __init__(self, pid, arrival_time, burst_time):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.completion_time = 0
        self.waiting_time = 0
        self.turnaround_time = 0

def fcfs_scheduling(processes):
    time = 0
    gantt_chart = []

    # Sort processes based on arrival time
    sorted_processes = sorted(processes, key=lambda x: x.arrival_time)

    for process in sorted_processes:
        if time < process.arrival_time:
            time = process.arrival_time  # If the CPU is idle, move the time forward to the arrival time of the next process
        gantt_chart.extend([process.pid] * process.burst_time)
        time += process.burst_time
        process.completion_time = time
        process.turnaround_time = process.completion_time - process.arrival_time
        process.waiting_time = process.turnaround_time - process.burst_time

    return sorted_processes, gantt_chart

def print_processes(processes):
    print("PID\tArrival\tBurst\tCompletion\tWaiting\tTurnaround")
    for process in processes:
        print(f"{process.pid}\t{process.arrival_time}\t{process.burst_time}\t{process.completion_time}\t{process.waiting_time}\t{process.turnaround_time}")

def print_gantt_chart(gantt_chart):
    print("\nGantt Chart:")
    for pid in gantt_chart:
        print(f"| P{pid} ", end="")
    print("|")
    for i in range(len(gantt_chart)):
        print(f" {i}  ", end="")
    print(f" {len(gantt_chart)}")

if __name__ == "__main__":
    processes = [
        Process(1, 0, 8),
        Process(2, 1, 4),
        Process(3, 2, 9),
        Process(4, 3, 5)
    ]

    processes, gantt_chart = fcfs_scheduling(processes)
    print_processes(processes)
    print_gantt_chart(gantt_chart)