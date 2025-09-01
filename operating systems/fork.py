import multiprocessing

from click import clear

def worker(i):
    print(f"Hello from process {i}")

def main():
    processes = []
    for i in range(1, 5):
        p = multiprocessing.Process(target=worker, args=(i,))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

if __name__ == "__main__":
    main()