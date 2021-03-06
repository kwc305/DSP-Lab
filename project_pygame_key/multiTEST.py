import multiprocessing
import time

def worker(input_name):
    name = multiprocessing.current_process().name
    print name, 'Starting'
    print input_name
    time.sleep(2)
    print name, 'Exiting'

def my_service():
    name = multiprocessing.current_process().name
    print name, 'myserviceStarting'
    time.sleep(3)
    print name, 'myserviceExiting'

if __name__ == '__main__':
    service = multiprocessing.Process(name='my_service',
                                      target=my_service)
    worker_1 = multiprocessing.Process(name='worker 1',
                                       target=worker,
                                       args=('11',))
    worker_2 = multiprocessing.Process(name='worker2',
                                        target=worker,
                                        args=('22',)) # default name

    worker_1.start()
    time.sleep(1)
    worker_2.start()
    service.start()