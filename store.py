class Store:
    def __init__(self):
        self.store = {}
        pass

    def get(self, key, value):
        return self.store[key]

    def set(self, key):
        self.store[key] = value

    def delete(self, key):
        del self.store[key]

    def show(self):
        return self.store
