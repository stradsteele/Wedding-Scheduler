class Wedding:
    def __init__(self, wedding_id, couple_name, date, start_time, end_time, num_guests):
        self.wedding_id = wedding_id
        self.couple_name = couple_name
        self.date = date
        self.start_time = start_time
        self.end_time = end_time
        self.num_guests = num_guests  # Número total de invitados
        self.num_tables = self.calculate_tables(num_guests)  # Se calcula automáticamente
        self.tables_assigned = []  # Lista de IDs de mesas asignadas
        self.waiters_assigned = []  # Lista de IDs de meseros asignados
        self.menu_type = None  # Tipo de menú para toda la boda
        
    def calculate_tables(self, num_guests):
        """Calcula el número de mesas necesarias (5 invitados por mesa)"""
        tables_needed = num_guests // 5
        if num_guests % 5 > 0:
            tables_needed += 1
        return min(tables_needed, 20)  # Máximo 20 mesas
        
    def assign_menu(self, menu_type):
        """Asigna un tipo de menú a toda la boda"""
        self.menu_type = menu_type
        
    def to_dict(self):
        return {
            "wedding_id": self.wedding_id,
            "couple_name": self.couple_name,
            "date": self.date,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "num_guests": self.num_guests,
            "num_tables": self.num_tables,
            "tables_assigned": self.tables_assigned,
            "waiters_assigned": self.waiters_assigned,
            "menu_type": self.menu_type
        }
    
    @classmethod
    def from_dict(cls, data):
        wedding = cls(
            data["wedding_id"],
            data["couple_name"],
            data["date"],
            data["start_time"],
            data["end_time"],
            data["num_guests"]
        )
        wedding.tables_assigned = data.get("tables_assigned", [])
        wedding.waiters_assigned = data.get("waiters_assigned", [])
        wedding.menu_type = data.get("menu_type")
        return wedding