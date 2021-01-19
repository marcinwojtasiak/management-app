class Transaction:
    def __init__(self, value, date, item):
        self.value = value
        self.date = date
        self.item = item

    def __iter__(self):
        for var in [self.value, self.date, self.item]:
            yield var
