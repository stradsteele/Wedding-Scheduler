class Waiter:
    def __init__(self, waiter_id, name):
        self.waiter_id = waiter_id
        self.name = name
        self.assigned_tables = []  # Lista de IDs de mesas (máx 4)
        
    def assign_table(self, table_id):
        if len(self.assigned_tables) < 4:
            self.assigned_tables.append(table_id)
            return True
        return False
    
    def remove_table(self, table_id):
        if table_id in self.assigned_tables:
            self.assigned_tables.remove(table_id)
            return True
        return False
    
    def to_dict(self):
        return {
            "waiter_id": self.waiter_id,
            "name": self.name,
            "assigned_tables": self.assigned_tables
        }
    
    @classmethod
    def from_dict(cls, data):
        waiter = cls(data["waiter_id"], data["name"])
        waiter.assigned_tables = data["assigned_tables"]
        return waiter