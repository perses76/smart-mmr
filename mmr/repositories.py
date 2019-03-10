class ItemNotFoundException(RuntimeError):
    def __init__(self, repository_code, item_code):
        self.repository_code = repository_code
        self.item_code = item_code

    def __str__(self):
        return f"Can not find item with code: '{self.item_code}' in repository: '{self.repository_code}'"


class Repositories():
    def __init__(self, programs, channels, airlines):
        self.programs = programs
        self.channels = channels
        self.airlines = airlines


class Repository():
    def __init__(self, code, items):
        self.code = code
        self.items = items

    def __iter__(self):
        return self.items.__iter__()

    def __getitem__(self, code):
        for item in self:
            if item.code == code:
                return item
        raise ItemNotFoundException(self.code, code)
