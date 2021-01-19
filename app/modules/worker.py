class Worker:
    def __init__(self, name, surname, tel):
        self.name = name
        self.surname = surname
        self.tel = tel

    def __iter__(self):
        for var in [self.name, self.surname, self.tel]:
            yield var
