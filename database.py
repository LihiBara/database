class Database():
    def _init_(self):
        """
        initializer
        """
        self.dict = {}

    def set_value(self, key, val):
        self.dict[key] = val
        if key in self.dict.keys():
            return True
        else:
            return False

    def get_value(self, key):
        if key in self.dict.keys():
            return self.dict[key]
        else:
            raise

    def delete_value(self, key):
        if key in self.dict.keys():
            value = self.get_value(key)
            del self.dict[key]
            return value


db = Database()
db.set_value("a", "b")

print(db.dict)