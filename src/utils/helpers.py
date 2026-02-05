import re
from datetime import datetime

class InputValidator:
    @staticmethod
    def validate_time(time_str):
        """Valida que el formato de hora sea HH:MM (24h)"""
        if not re.match(r'^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$', time_str):
            return False
        
        # Verificar que no sea hora inválida como 25:00
        try:
            datetime.strptime(time_str, "%H:%M")
            return True
        except ValueError:
            return False
    
    @staticmethod
    def validate_date(date_str):
        """Valida que el formato de fecha sea YYYY-MM-DD"""
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False
    
    @staticmethod
    def validate_positive_int(value, max_value=None):
        """Valida que el valor sea un entero positivo"""
        try:
            num = int(value)
            if num <= 0:
                return False
            if max_value and num > max_value:
                return False
            return True
        except ValueError:
            return False

class MenuGenerator:
    MENU_OPTIONS = {
        "1": {"name": "Clásico", "description": "Pasta + Vino tinto + Postre tradicional"},
        "2": {"name": "Vegetariano", "description": "Lasagna veggie + Vino blanco + Postre sin lactosa"},
        "3": {"name": "Premium", "description": "Filete + Champagne + Postre gourmet"},
        "4": {"name": "Económico", "description": "Pollo + Refrescos + Flan casero"}
    }
    
    @staticmethod
    def display_menu_options():
        """Muestra las opciones de menú disponibles"""
        print("\n--- OPCIONES DE MENÚ ---")
        for key, menu in MenuGenerator.MENU_OPTIONS.items():
            print(f"{key}. {menu['name']}")
            print(f"   {menu['description']}")
        print()
    
    @staticmethod
    def get_menu_by_choice(choice):
        """Obtiene el menú según la elección"""
        return MenuGenerator.MENU_OPTIONS.get(choice, {"name": "Personalizado", "description": "Menú a medida"})