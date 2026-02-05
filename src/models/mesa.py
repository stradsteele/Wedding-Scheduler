class Table:
    def __init__(self, table_id, wedding_id):
        self.table_id = table_id
        self.wedding_id = wedding_id
        self.food_beverage = None  # Menú asignado
        self.waiter_id = None  # ID del mesero asignado
        self.guests = []  # Lista de nombres de invitados (máx 5)
        
    def add_guest(self, guest_name):
        if len(self.guests) < 5:
            self.guests.append(guest_name)
            return True
        return False
    
    def assign_food_beverage(self, menu):
        self.food_beverage = menu
        
    def assign_waiter(self, waiter_id):
        self.waiter_id = waiter_id
        
    def to_dict(self):
        return {
            "table_id": self.table_id,
            "wedding_id": self.wedding_id,
            "food_beverage": self.food_beverage,
            "waiter_id": self.waiter_id,
            "guests": self.guests
        }
    
    @classmethod
    def from_dict(cls, data):
        table = cls(data["table_id"], data["wedding_id"])
        table.food_beverage = data["food_beverage"]
        table.waiter_id = data["waiter_id"]
        table.guests = data["guests"]
        return table