def main():
    table = [
        ["P1", 2,  6], 
        ["P2", 5,  2], 
        ["P3", 1,  8], 
        ["P4", 0,  3], 
        ["P5", 4,  4]
    ]
    sjf(table)
    
def sjf(table):
    table.sort(key=lambda x: x[1])
    table = [x + [0 for i in range(3)] for x in table]
    
    current_time = 0
    completed = 0
    ready_queue = []
    
    while completed < len(table):
        for process in table:
            if process[1] <= current_time and process not in ready_queue and process[3] == 0:
                ready_queue.append(process)
        
        if not ready_queue:
            current_time += 1
            continue
        
        ready_queue.sort(key=lambda x: x[2])
        
        current_process = ready_queue.pop(0)
        
        current_time += current_process[2]
        current_process[3] = current_time
        
        current_process[4] = current_process[3] - current_process[1] - current_process[2]
        current_process[5] = current_process[3] - current_process[1]
        
        completed += 1
    
    print("Gantt chart:")
    print("0", end="")
    for process in sorted(table, key=lambda x: x[3]):
        print(f" -> {process[0]} -> {process[3]}", end="")
    print()
    
    print("\nTable:")        
    for i in ["ProcessID","ArrivalTime", "BurstTime", "CompletionTime", "WaitingTime", "TurnaroundTime"]:
        print(f"{i:<15}", end="")
    print()      
    for process in table:
        for item in process:
            print(f"{item:<15}", end="")
        print()
    
    avg_waiting_time = sum([x[4] for x in table]) / len(table)
    avg_turnaround_time = sum([x[5] for x in table])
    
    print(f"\nAverage waiting time: {avg_waiting_time:.2f}")
    print(f"Average turnaround time: {avg_turnaround_time:.2f}")
    
if __name__ == "__main__":
    main()
