import json
import os
from datetime import datetime

class WeddingDatabase:
    def __init__(self, file_path="data/weddings.json"):
        self.file_path = file_path
        self.weddings = []
        self.load_data()
        
    def load_data(self):
        """Carga los datos desde el archivo JSON"""
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, 'r', encoding='utf-8') as file:
                    self.weddings = json.load(file)
            except (json.JSONDecodeError, FileNotFoundError):
                self.weddings = []
        else:
            # Crear archivo vacío si no existe
            self.weddings = []
            self.save_data()
    
    def save_data(self):
        """Guarda los datos en el archivo JSON"""
        with open(self.file_path, 'w', encoding='utf-8') as file:
            json.dump(self.weddings, file, indent=4, ensure_ascii=False)
    
    def add_wedding(self, wedding_data):
        """Añade una nueva boda a la base de datos"""
        self.weddings.append(wedding_data)
        self.save_data()
        return True
    
    def update_wedding(self, wedding_id, updated_data):
        """Actualiza los datos de una boda existente"""
        for i, wedding in enumerate(self.weddings):
            if wedding["wedding_id"] == wedding_id:
                self.weddings[i] = updated_data
                self.save_data()
                return True
        return False
    
    def delete_wedding(self, wedding_id):
        """Elimina una boda de la base de datos"""
        for i, wedding in enumerate(self.weddings):
            if wedding["wedding_id"] == wedding_id:
                del self.weddings[i]
                self.save_data()
                return True
        return False
    
    def get_wedding(self, wedding_id):
        """Obtiene una boda por su ID"""
        for wedding in self.weddings:
            if wedding["wedding_id"] == wedding_id:
                return wedding
        return None
    
    def get_all_weddings(self):
        """Obtiene todas las bodas"""
        return self.weddings
    
    def check_schedule_conflict(self, new_wedding):
        """Verifica si hay conflicto de horario con bodas existentes"""
        for wedding in self.weddings:
            # Solo verificar si es el mismo día y no es la misma boda
            if wedding["date"] == new_wedding["date"]:
                try:
                    # Convertir tiempos a objetos datetime para comparar
                    existing_start = datetime.strptime(wedding["start_time"], "%H:%M")
                    existing_end = datetime.strptime(wedding["end_time"], "%H:%M")
                    new_start = datetime.strptime(new_wedding["start_time"], "%H:%M")
                    new_end = datetime.strptime(new_wedding["end_time"], "%H:%M")
                    
                    # Verificar superposición (excluyendo límites exactos)
                    if (new_start < existing_end and new_end > existing_start):
                        return True
                except ValueError:
                    # Si hay error en el formato, continuar
                    continue
        return False