class EntityCollection:
    def __init__(self):
        self._items = []

    @property
    def items(self):
        return self._items

    def add(self, entity):
        self._items.append(entity)

    def find_by_id(self, entity_id):
        for item in self._items:
            if item.id == entity_id:
                return item
        return None

    def list_all(self, title):
        print(f"\n**** {title} ****")
        for item in self._items:
            item.list()

    def input_multiple(self, entity_class, count):
        for _ in range(count):
            entity = entity_class()
            entity.input()
            self.add(entity)

    def input_multiple_gui(self, entity_class, count):
        """Input multiple entities via GUI"""
        for _ in range(count):
            entity = entity_class()
            if entity.input_gui():
                self.add(entity)
