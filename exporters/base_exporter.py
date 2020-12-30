class BaseExporter:
    def __init__(self):
        pass

    async def export(self, kahoot):
        raise NotImplementedError()
