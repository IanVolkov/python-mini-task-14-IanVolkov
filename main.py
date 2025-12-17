from typing import NamedTuple
import numpy as np
import threading as th
import time
from functools import wraps
import sys


class Task:
    total_tasks_created = 0
    def __init__(self, size, value, times):
        Task.total_tasks_created += 1
        self.size = size
        self.value = value
        self.times = times

def producer(query, amount_of_tasks):
    global is_ended
    for i in range(amount_of_tasks):
        with lock:
            query.append(Task(Task.total_tasks_created + 1, 42, 6))
    is_ended = True


def consumer(query):
    global is_ended
    while not is_ended or len(query) != 0:
        if len(query) == 0:
            continue
        with lock:
            task = query.pop(0)
        new_matrix = np.array([[task.value ** (i + j) for j in range(task.size)] for i in range(task.size)])
        np.linalg.matrix_power(new_matrix, task.times).sum()
        
def time_single_run(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Function '{func.__name__}' took " \
        f"{end_time - start_time:.4f} seconds.")
        return result
    return wrapper

@time_single_run
def multi_thread():
    prod_tr = th.Thread(target=producer, args=(query, amount_of_tasks))
    cons_treads = [th.Thread(target=consumer, args=(query,)) for _ in range(amount_of_consumers)]
    prod_tr.start()
    for tr in cons_treads: tr.start()
    prod_tr.join()
    for tr in cons_treads: tr.join()
    

if __name__ == "__main__":
    is_ended = False
    lock = th.Lock()
    query = []
    amount_of_tasks = 50
    amount_of_consumers = int(sys.argv[1])
    print(f"With {amount_of_consumers} consumers:")
    multi_thread()
