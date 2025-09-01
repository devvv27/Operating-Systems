class Process:
    def __init__(self, pid, burst_time, priority, arrival_time):
        self.pid = pid
        self.burst_time = burst_time
        self.priority = priority
        self.arrival_time = arrival_time
        self.remaining_time = burst_time
        self.completion_time = 0
        self.waiting_time = 0
        self.turnaround_time = 0

def preemptive_priority_scheduling(processes):
    time = 0
    completed = 0
    n = len(processes)
    gantt_chart = []
    
    while completed != n:
        # Find the process with the highest priority (lowest priority number) that has arrived and is not completed
        idx = -1
        highest_priority = float('inf')
        for i in range(n):
            if processes[i].arrival_time <= time and processes[i].remaining_time > 0 and processes[i].priority < highest_priority:
                highest_priority = processes[i].priority
                idx = i
 
        if idx != -1:
            processes[idx].remaining_time -= 1
            gantt_chart.append(processes[idx].pid)
            time += 1
            if processes[idx].remaining_time == 0:
                processes[idx].completion_time = time
                processes[idx].turnaround_time = processes[idx].completion_time - processes[idx].arrival_time
                processes[idx].waiting_time = processes[idx].turnaround_time - processes[idx].burst_time
                completed += 1
        else:
            gantt_chart.append(None)
            time += 1

    return processes, gantt_chart

def print_processes(processes):
    total_waiting_time = 0
    total_turnaround_time = 0
    print("PID\tBurst Time\tPriority\tArrival Time\tCompletion Time\tWaiting Time\tTurnaround Time")
    for process in processes:
        total_waiting_time += process.waiting_time
        total_turnaround_time += process.turnaround_time
        print(f"{process.pid}\t{process.burst_time}\t\t{process.priority}\t\t{process.arrival_time}\t\t{process.completion_time}\t\t{process.waiting_time}\t\t{process.turnaround_time}")
    
    avg_waiting_time = total_waiting_time / len(processes)
    avg_turnaround_time = total_turnaround_time / len(processes)
    print(f"\nAverage Waiting Time: {avg_waiting_time}")
    print(f"Average Turnaround Time: {avg_turnaround_time}")

def print_gantt_chart(gantt_chart):
    print("\nGantt Chart:")
    for pid in gantt_chart:
        if pid is not None:
            print(f"P{pid}", end=" ")
        else:
            print("Idle", end=" ")
    print()

# Example usage
processes = [
    Process(1, 10, 3, 0),
    Process(2, 1, 1, 2),
    Process(3, 2, 4, 4),
    Process(4, 1, 5, 6),
    Process(5, 5, 2, 8)
]

scheduled_processes, gantt_chart = preemptive_priority_scheduling(processes)
print_processes(scheduled_processes)
print_gantt_chart(gantt_chart)