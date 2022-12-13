"""
author: Lihi Baranetz
checks the synchronization while mode is processing
"""
from filedb import Filedb
from sync import Syncdb
from multiprocessing import Process
import logging


def reader(database):
    """
    a reader try to get an access to read the value from the dictionary
    :param database: dictionary
    """
    logging.debug("reader started")
    for i in range(100):
        flag = database.get_value(i) is None or database.get_value(i) == i

        assert flag
    logging.debug("reader left")


def writer(database):
    """
    writer try to get an access to write the value from the dictionary
    :param database: an object that one of his feature is a dictionary
    """
    logging.debug("writer started")
    for i in range(100):
        assert database.set_value(i, i)
    for i in range(100):
        flag = database.delete_value(i) == i or database.delete_value(i) is None
        assert flag
    logging.debug("writer left")


def main():
    """
    main function
    """
    #  checks the access of writing and reading without competition
    logging.basicConfig(filename='log_process.txt', level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(threadName)s %(message)s')
    database = Syncdb(Filedb(), False)
    all_processes = []
    for i in range(0, 50):
        proc = Process(target=reader, args=(database, ))
        all_processes.append(proc)
    for i in range(0, 10):
        proc = Process(target=writer, args=(database, ))
        all_processes.append(proc)
    for i in all_processes:
        i.start()
    for i in all_processes:
        i.join()


if __name__ == "__main__":
    main()
