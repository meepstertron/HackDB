from rq import get_current_job
import time


# me testing the task queue
def example_task(x, y):
    job = get_current_job()
    print(f"Running example_task with args: {x}, {y}")
    time.sleep(2)  
    result = x + y
    print(f"Task result: {result}")
    return result
