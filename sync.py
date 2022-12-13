import threading
import multiprocessing
from filedb import Filedb
import logging


class Syncdb:
    def __init__(self, database: Filedb, thread_or_process):
        """
        initializer
        :param database: dictionary
        :param thread_or_process: true/false for thread/process
        """
        if not isinstance(database, Filedb):
            raise ValueError("not filedb instance")
        self.database = database
        if thread_or_process:
            self.semaphore = threading.Semaphore(10)
            self.lock = threading.Lock()
        else:
            self.semaphore = multiprocessing.Semaphore(10)
            self.lock = multiprocessing.Lock()

    def get_value(self, key):
        """
        allows up to 10 readers to read at the same time
        :param key: key of the dictionary
        :return: the key's value
        """
        self.semaphore.acquire()
        logging.debug("reader in")
        value = self.database.get_value(key)
        self.semaphore.release()
        logging.debug("reader out")
        return value

    def set_value(self, key, val):
        """
        allows one writer to set a new value in the dictionary while nobody else allowed in.
        :param key: key of the dictionary
        :param val: the new value for the dictionary
        :return: True if value has been added, if not False
        """
        self.lock.acquire()
        for i in range(10):
            self.semaphore.acquire()
        logging.debug("writer in")
        flag = self.database.set_value(key, val)
        for i in range(10):
            self.semaphore.release()
        logging.debug("writer out")
        self.lock.release()
        return flag

    def delete_value(self, key):
        """
        allows one user to delete a value from the dictionary while nobody else allowed in.
        :param key: key of the dictionary
        :return: the deleted value
        """
        self.lock.acquire()
        for i in range(10):
            self.semaphore.acquire()
        flag = self.database.delete_value(key)
        self.lock.release()
        for i in range(10):
            self.semaphore.release()
        return flag
