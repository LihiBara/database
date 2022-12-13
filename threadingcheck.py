"""
author: Lihi Baranetz
checks the synchronization while mode is processing
"""
from filedb import Filedb
from sync import Syncdb
from threading import Thread
import logging


def reader(database):
    """
    a reader try to get an access to read the value from the dictionary
    :param database: an object that one of his feature is a dictionary
    """
    logging.debug("reader started")
    for i in range(100):
        flag = database.get_value(i) == i or database.get_value(i) is None
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
        val = database.delete_value(i)
        flag = val == i or val is None
        assert flag
    logging.debug("writer left")


def main():
    """
    main function
    """
    logging.basicConfig(filename='log_thread.txt', level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(threadName)s %(message)s')
    database = Syncdb(Filedb(), True)
    all_threads = []
    for i in range(400, 500):
        database.set_value(i, i)
    for i in range(0, 50):
        thread = Thread(target=reader, args=(database, ))
        all_threads.append(thread)
    for i in range(0, 10):
        thread = Thread(target=writer, args=(database, ))
        all_threads.append(thread)
    for i in all_threads:
        i.start()
    for i in all_threads:
        i.join()
    for i in range(400, 500):
        assert database.get_value(i) == i


if __name__ == "__main__":
    main()
