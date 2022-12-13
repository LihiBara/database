from database import Database
import pickle


class Filedb(Database):
    def __init__(self):
        """
        initializer
        """
        super().__init__()

    def dump(self):
        """
        writes the dictionary in the file
        """
        with open("dbfile.txt", "wb") as file:
            pickle.dump(self.dict, file)
        # Pickling the dict and writing in a file

    def set_value(self, key, val):
        """
        set a new value in the dictionary file
        :param key: key of the dictionary
        :param val: the new value for the dictionary
        :return: True if value has been added, if not False
        """
        self.load()
        flag = super().set_value(key, val)
        self.dump()
        return flag

    def get_value(self, key):
        """
        gets the value from the dictionary file
        :param key: key of the dictionary
        :return: The value of the key from the dictionary file
        """
        self.load()
        return super().get_value(key)

    def load(self):
        """
        put the written in the file back into the dictionary
        """
        with open("dbfile.txt", "rb") as file:
            self.dict = pickle.load(file)
        # Unpickling the object

    def delete_value(self, key):
        """
        deletes the value of the key from the dictionary file
        :param key: key of the dictionary
        :return: the value that was deleted
        """
        self.load()
        val = super().delete_value(key)
        self.dump()
        return val
