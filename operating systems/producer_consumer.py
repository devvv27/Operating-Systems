import time
import threading

N = 10

buf = [0] * N

fill_count = threading.Semaphore(0)
empty_count = threading.Semaphore(N)

item_counter = 0
item_counter_lock = threading.Lock()

def produce():
    global item_counter
    with item_counter_lock:
        item_counter += 1
        item_id = item_counter
    print(f"Item {item_id} produced!")
    return item_id

def producer():
    front = 0
    while True:
        x = produce()
        empty_count.acquire()
        buf[front] = x
        fill_count.release()
        print(f"Buffer after producing: {buf}")
        front = (front + 1) % N
        time.sleep(0.5) 

def consume(y):
    print(f"Item {y} consumed!")

def consumer():
    rear = 0
    while True:
        fill_count.acquire()
        y = buf[rear]
        empty_count.release()
        consume(y)
        print(f"Buffer after consuming: {buf}")  
        rear = (rear + 1) % N
        time.sleep(0.5)  

producer_thread = threading.Thread(target=producer)
consumer_thread = threading.Thread(target=consumer)

producer_thread.start()
consumer_thread.start()