from database import Database
import pickle


class Filedb(Database):
    def _init_(self):
        """
        initializer

        """
        super()._init_()

    def dump(self):
        with open("dbfile.txt", "wb") as file:
            pickle.dump(self.dict, file)
        # Pickling the dict and writing in a file

    def set_value(self, key, val):
        self.load()
        flag = super().set_value(key, val)
        self.dump()
        return flag

    def get_value(self, key):
        self.load()
        return super().get_value(key)

    def load(self):
        with open("dbfile.txt", "rb") as file:
            self.dict = pickle.load(file)
        # Unpickling the object


db = Filedb()
db.dump()