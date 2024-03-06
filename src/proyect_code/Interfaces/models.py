# interfaces.py


class IDocument:
    def __init__(self, id: int, title: str):
        self.id = id
        self.title = title


class IData:
    def __init__(self, name: str, standar: int, extended: int):
        self.name = name
        self.standar = standar
        self.extended = extended


class IMetrics:
    def __init__(self, data: list):
        self.data = data


class IQuery:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name
