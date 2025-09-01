import time
class Process:
    def __init__(self, pid, arrivalTime, burstTime, priority=-1):
        self.pid = pid
        self.burstTime = burstTime
        self.arrivalTime = arrivalTime
        self.waitingTime = 0
        self.turnAroundTime = 0
        self.priority = priority
        self.timeRemaining = burstTime

    def __str__(self):
        return f"P{self.pid}"

class CPU:
    def __init__(self, processList:list) -> None:
        self.processList = processList

    def reset(self):
        for process in self.processList:
            process.waitingTime = 0
            process.turnAroundTime = 0
            process.timeRemaining = process.burstTime

    def fcfs(self):
        sortedList = sorted(self.processList, key=lambda x: x.arrivalTime)
        totalTime = sortedList[0].arrivalTime
        for process in sortedList:
            if totalTime < process.arrivalTime:
                process.waitingTime = process.arrivalTime
            elif totalTime!=0:
                process.waitingTime = totalTime-process.arrivalTime
            else:
                process.waitingTime = 0 
            process.turnAroundTime = process.burstTime + process.waitingTime
            totalTime += process.burstTime 
        
        totalWaiting = totalTurnAroundTime = 0
        print("FCFS")
        print("----")
        print("PID","AT","BT","WT","TAT",sep="\t")
        for process in self.processList:
            print(f"P{process.pid}",process.arrivalTime, process.burstTime, 
                  process.waitingTime, process.turnAroundTime, sep="\t")
            totalWaiting += process.waitingTime
            totalTurnAroundTime += process.turnAroundTime
        print("Avg. Waiting Time: ", round(totalWaiting/len(self.processList), 2))
        print("Avg. Turn Around Time: ", round(totalTurnAroundTime/len(self.processList), 2))

    def sjf(self):  
        sortedList = sorted(self.processList, key=lambda x: x.burstTime)
        readyQueue = []
        totalTime = min(self.processList, key=lambda x: x.arrivalTime).arrivalTime
        while sortedList:
            while True:
                t1 = list(filter(lambda x: x.arrivalTime <= totalTime, sortedList))
                t2 = list(filter(lambda x: x.arrivalTime > totalTime, sortedList))
                # print([i.pid for i in t1], [i.pid for i in t2])
                if t1:
                    current = t1.pop(0)
                    totalTime += current.burstTime
                    current.turnAroundTime = totalTime-current.arrivalTime
                    current.waitingTime = current.turnAroundTime - current.burstTime
                elif t2:
                    t2.sort(key=lambda x:x.arrivalTime)
                    current = t2.pop(0)
                    totalTime += (current.arrivalTime - totalTime) + current.burstTime
                    current.waitingTime = 0
                    current.turnAroundTime = current.burstTime
                    t2.clear()

                
                readyQueue.append(current)
                sortedList.remove(current)
                if not t1 and not t2:
                    break
                
        
        totalWaiting = totalTurnAroundTime = 0
        print("SJF")
        print("---")
        print("PID","AT","BT","WT","TAT",sep="\t")
        for process in self.processList:
            print(f"P{process.pid}",process.arrivalTime, process.burstTime, 
                  process.waitingTime, process.turnAroundTime, sep="\t")
            totalWaiting += process.waitingTime
            totalTurnAroundTime += process.turnAroundTime
        print("Avg. Waiting Time: ", round(totalWaiting/len(self.processList), 2))
        print("Avg. Turn Around Time: ", round(totalTurnAroundTime/len(self.processList), 2))

    def npp(self):
        sortedList = sorted(self.processList, key=lambda x: x.arrivalTime)
        readyQueue = []
        totalTime = min(self.processList, key=lambda x: x.arrivalTime).arrivalTime
        while sortedList:
            while True:
                t1 = list(filter(lambda x: x.arrivalTime <= totalTime, sortedList))
                t2 = list(filter(lambda x: x.arrivalTime > totalTime, sortedList))
                # print([i.pid for i in t1], [i.pid for i in t2])
                if t1:
                    t1.sort(key=lambda x:x.priority)
                    current = t1.pop(0)
                    totalTime += current.burstTime
                    current.turnAroundTime = totalTime-current.arrivalTime
                    current.waitingTime = current.turnAroundTime - current.burstTime
                elif t2:
                    t2.sort(key=lambda x:x.priority)
                    current = t2.pop(0)
                    totalTime += (current.arrivalTime - totalTime) + current.burstTime
                    current.waitingTime = 0
                    current.turnAroundTime = current.burstTime
                    t2.clear()

                
                readyQueue.append(current)
                sortedList.remove(current)
                if not t1 and not t2:
                    break
                
        
        totalWaiting = totalTurnAroundTime = 0
        print("NPP")
        print("---")
        print("PID","AT","BT", "PT","WT","TAT",sep="\t")
        for process in self.processList:
            print(f"P{process.pid}",process.arrivalTime, process.burstTime, 
                  process.priority, process.waitingTime, process.turnAroundTime, sep="\t")
            totalWaiting += process.waitingTime
            totalTurnAroundTime += process.turnAroundTime
        print("Avg. Waiting Time: ", round(totalWaiting/len(self.processList), 2))
        print("Avg. Turn Around Time: ", round(totalTurnAroundTime/len(self.processList), 2))

    def pp(self):
        sortedList = sorted(self.processList, key=lambda x: (x.arrivalTime, x.priority, x.pid))
        interrupted = []
        waiting = set()
        totalTime = sortedList[0].arrivalTime
        current = sortedList.pop(0)

        while sortedList or waiting or interrupted or current:
            if not current and not waiting and sortedList:
                totalTime = sortedList[0].arrivalTime
                current = sortedList.pop(0)
                continue
            totalTime += 1
            
            if current:
                current.timeRemaining -= 1
                
                # print(totalTime, [i.pid for i in sortedList], [i.pid for i in interrupted], current, "->", current.timeRemaining)

                if current.timeRemaining == 0:
                    current.turnAroundTime = totalTime - current.arrivalTime
                    current.waitingTime = current.turnAroundTime - current.burstTime
                    #print(f"Process {current.pid} finished. TAT: {current.turnAroundTime}, WT: {current.waitingTime}")
                    current = None 

            newlyArrived = [p for p in sortedList if p.arrivalTime <= totalTime]
            sortedList = [p for p in sortedList if p.arrivalTime > totalTime]
            waiting.update(newlyArrived)

            if not current:
                if waiting or interrupted:
                    availableProcesses = sorted(list(waiting) + interrupted, key=lambda p: (p.priority, p.arrivalTime, p.pid))
                    current = availableProcesses[0]
                    if current in waiting:
                        waiting.remove(current)
                    elif current in interrupted:
                        interrupted.remove(current)
            
            elif current:
                availableProcesses = sorted(list(waiting) + interrupted, key=lambda p: (p.priority, p.arrivalTime, p.pid))
                if availableProcesses:
                    highestPriorityProcess = availableProcesses[0]
                    
                    if highestPriorityProcess.priority < current.priority:
                        # print(f"Preempting Process {current.pid} with Process {highestPriorityProcess.pid}")
                        interrupted.append(current)
                        current = highestPriorityProcess

                        if current in waiting:
                            waiting.remove(current)
                        elif current in interrupted:
                            interrupted.remove(current)
            
            

        totalWaiting = totalTurnAroundTime = 0
        print("PP")
        print("---")
        print("PID","AT","BT", "PT","WT","TAT",sep="\t")
        for process in self.processList:
            print(f"P{process.pid}",process.arrivalTime, process.burstTime, 
                process.priority, process.waitingTime, process.turnAroundTime, sep="\t")
            totalWaiting += process.waitingTime
            totalTurnAroundTime += process.turnAroundTime
        print("Avg. Waiting Time: ", round(totalWaiting/len(self.processList), 2))
        print("Avg. Turn Around Time: ", round(round(totalTurnAroundTime/len(self.processList), 2), 2))
        
    def strn(self):
        sortedList = sorted(self.processList, key=lambda x: (x.arrivalTime, x.timeRemaining, x.pid))
        interrupted = []
        waiting = set()
        totalTime = sortedList[0].arrivalTime
        current = sortedList.pop(0)

        while sortedList or waiting or interrupted or current:
            totalTime += 1
            
            if current:
                current.timeRemaining -= 1
                # print(totalTime, [i.pid for i in sortedList], [i.pid for i in interrupted], current, "->", current.timeRemaining)

                if current.timeRemaining == 0:
                    current.turnAroundTime = totalTime - current.arrivalTime
                    current.waitingTime = current.turnAroundTime - current.burstTime
                    # print(f"Process {current.pid} finished. TAT: {current.turnAroundTime}, WT: {current.waitingTime}")
                    current = None

            newlyArrived = [p for p in sortedList if p.arrivalTime <= totalTime]
            sortedList = [p for p in sortedList if p.arrivalTime > totalTime]
            waiting.update(newlyArrived)

            if not current:
                if waiting or interrupted:
                    availableProcesses = sorted(list(waiting) + interrupted, key=lambda p: (p.timeRemaining, p.pid))
                    current = availableProcesses[0]
                    if current in waiting:
                        waiting.remove(current)
                    elif current in interrupted:
                        interrupted.remove(current)

            elif current:
                availableProcesses = sorted(list(waiting) + interrupted, key=lambda p: (p.timeRemaining, p.pid))
                if availableProcesses:
                    shortestProcess = availableProcesses[0]
                    
                    if shortestProcess.timeRemaining < current.timeRemaining:
                        #print(f"Preempting Process {current.pid} with Process {shortestProcess.pid}")
                        interrupted.append(current)
                        current = shortestProcess
                        if current in waiting:
                            waiting.remove(current)
                        elif current in interrupted:
                            interrupted.remove(current)


        totalWaiting = totalTurnAroundTime = 0
        print("SRTN")
        print("---")
        print("PID","AT","BT", "WT","TAT",sep="\t")
        for process in self.processList:
            print(f"P{process.pid}",process.arrivalTime, process.burstTime, 
                  process.waitingTime, process.turnAroundTime, sep="\t")
            totalWaiting += process.waitingTime
            totalTurnAroundTime += process.turnAroundTime
        print("Avg. Waiting Time: ", round(totalWaiting/len(self.processList), 2))
        print("Avg. Turn Around Time: ", round(round(totalTurnAroundTime/len(self.processList), 2), 2))

    def roundRobin(self, quantum):
        sortedList = sorted(self.processList, key=lambda x: (x.arrivalTime, x.pid))
        readyQueue = []
        totalTime = sortedList[0].arrivalTime
        readyQueue.append(sortedList.pop(0))
        current = readyQueue.pop(0) if readyQueue else None

        while sortedList or readyQueue or current:
            # Handle idle CPU time
            if not current and not readyQueue and sortedList:
                totalTime += 1
                temp = list(filter(lambda x: x.arrivalTime <= totalTime, sortedList))
                if temp:
                    readyQueue.extend(temp)
                    sortedList = [p for p in sortedList if p.arrivalTime > totalTime]
                if readyQueue:
                    current = readyQueue.pop(0)
                continue

            # Handle current process
            if current:
                if current.timeRemaining > quantum:
                    totalTime += quantum
                    current.timeRemaining -= quantum
                    temp = [p for p in sortedList if p.arrivalTime <= totalTime]
                    readyQueue.extend(temp)
                    sortedList = [p for p in sortedList if p.arrivalTime > totalTime]
                    readyQueue.append(current)  # Add current back to the queue
                    current = readyQueue.pop(0) if readyQueue else None
                else:
                    totalTime += current.timeRemaining
                    current.turnAroundTime = totalTime - current.arrivalTime
                    current.waitingTime = current.turnAroundTime - current.burstTime
                    current.timeRemaining = 0
                    temp = [p for p in sortedList if p.arrivalTime <= totalTime]
                    readyQueue.extend(temp)
                    sortedList = [p for p in sortedList if p.arrivalTime > totalTime]
                    current = readyQueue.pop(0) if readyQueue else None

        totalWaiting = totalTurnAroundTime = 0
        print("Round Robin")
        print("---")
        print("PID","AT","BT", "WT","TAT",sep="\t")
        for process in self.processList:
            print(f"P{process.pid}",process.arrivalTime, process.burstTime, 
                process.waitingTime, process.turnAroundTime, sep="\t")
            totalWaiting += process.waitingTime
            totalTurnAroundTime += process.turnAroundTime
        print("Avg. Waiting Time: ", round(totalWaiting/len(self.processList), 2))
        print("Avg. Turn Around Time: ", round(round(totalTurnAroundTime/len(self.processList), 2), 2))
                
                


processList = [Process(1,1,5,3), Process(2,3,7,1), Process(3,2,2,2), 
                Process(4,0,4,5), Process(5,5,2,4), Process(6,4,8,2)]



c = CPU(processList)
c.fcfs()
print(); c.reset()
c.sjf()
print(); c.reset()
c.npp()
print(); c.reset()
c.pp()
print(); c.reset()
c.strn()
print(); c.reset()
c.roundRobin(3)