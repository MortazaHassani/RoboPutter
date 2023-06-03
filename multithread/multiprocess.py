import multiprocessing
## Printing number of cpu
#print("Number of cpu : ", multiprocessing.cpu_count())

from multiprocessing import Lock, Process, Queue, current_process
import time
import queue # imported for using queue.Empty exception


def do_job(to_process_q, processed_q):
    while True:
        try:
            '''
                try to get task from the queue. get_nowait() function will 
                raise queue.Empty exception if the queue is empty. 
                queue(False) function would do the same task also.
            '''
            task = to_process_q.get_nowait()
        except queue.Empty:

            break
        else:
            '''
                if no exception has been raised, add the task completion 
                message to task_that_are_done queue
            '''
            print(task)
            processed_q.put(task + ' is done by ' + current_process().name)
            time.sleep(.5)
    return True


def main():
    number_of_task = 10
    number_of_processes = multiprocessing.cpu_count() - 2
    to_process_q = Queue()
    processed_q = Queue()
    processes = []

    for i in range(number_of_task):
        to_process_q.put("Task no " + str(i))

    # creating processes
    for w in range(number_of_processes):
        p = Process(target=do_job, args=(to_process_q, processed_q))
        processes.append(p)
        p.start()

    # completing process
    for p in processes:
        p.join()

    # print the output
    while not processed_q.empty():
        print(processed_q.get())

    return True


if __name__ == '__main__':
    main()