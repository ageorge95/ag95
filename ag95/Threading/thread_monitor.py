from typing import List
from threading import Thread
from time import sleep

class ThreadMonitor:
    def __init__(self,
                 list_with_threads: List[Thread],
                 start_threads: bool = True):

        self.list_with_threads = list_with_threads
        self.start_threads = start_threads

    def watch_slave(self):
        # monitor all threads
        while True:
            if any([t.is_alive() for t in self.list_with_threads]):
                sleep(1)
            else:
                break
        print('ALL THREADS HAVE EXITED')

    def start_watching(self):
        if self.list_with_threads:
            if self.start_threads:
                # start all the provided threads
                for t in self.list_with_threads:
                    t.start()

            Thread(target=self.watch_slave).start()

if __name__ == '__main__':
    def my_worker_function(wait_time_s: int):
        sleep(wait_time_s)
        print(f'I have slept {wait_time_s}s')

    threads_list = [Thread(target=my_worker_function,
                           args=(1,)),
                    Thread(target=my_worker_function,
                           args=(2,)),
                    Thread(target=my_worker_function,
                           args=(3,))]

    ThreadMonitor(list_with_threads=threads_list).start_watching()

    print('MANUAL assessment required !')