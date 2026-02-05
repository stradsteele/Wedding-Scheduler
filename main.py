import os
import sys
import json
from datetime import datetime
from src.data.database import WeddingDatabase
from src.constraints.checker import ConstraintChecker
from src.utils.helpers import InputValidator, MenuGenerator

class WeddingPlannerApp:
    def __init__(self):
        self.db = WeddingDatabase()
        
    def clear_screen(self):
        """Limpia la pantalla de la consola"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_header(self):
        """Muestra el encabezado de la aplicación"""
        print("=" * 60)
        print("ORGANIZADOR DE BODAS - AGENCIA DE PLANIFICACIÓN")
        print("=" * 60)
    
    def main_menu(self):
        """Menú principal de la aplicación"""
        while True:
            self.clear_screen()
            self.display_header()
            print("\nMENÚ PRINCIPAL:")
            print("1. Crear nueva boda")
            print("2. Ver todas las bodas")
            print("3. Ver detalles de una boda")
            print("4. Eliminar una boda")
            print("5. Verificar restricciones")
            print("6. Salir")
            
            choice = input("\nSeleccione una opción (1-6): ")
            
            if choice == "1":
                self.create_wedding()
            elif choice == "2":
                self.view_all_weddings()
            elif choice == "3":
                self.view_wedding_details()
            elif choice == "4":
                self.delete_wedding()
            elif choice == "5":
                self.check_constraints()
            elif choice == "6":
                print("\n¡Gracias por usar el Organizador de Bodas!")
                sys.exit(0)
            else:
                print("\nOpción no válida. Intente de nuevo.")
                input("Presione Enter para continuar...")
    
    def create_wedding(self):
        """Crea una nueva boda"""
        self.clear_screen()
        self.display_header()
        print("\nCREAR NUEVA BODA\n")
        
        # Solicitar datos básicos
        wedding_id = input("ID de la boda (ej: B001): ").strip().upper()
        
        # Verificar si ya existe
        if self.db.get_wedding(wedding_id):
            print(f"\nError: Ya existe una boda con ID {wedding_id}")
            input("Presione Enter para continuar...")
            return
        
        couple_name = input("Nombres de la pareja: ").strip()
        
        # Fecha
        while True:
            date = input("Fecha de la boda (YYYY-MM-DD): ").strip()
            if InputValidator.validate_date(date):
                break
            print("Formato inválido. Use YYYY-MM-DD")
        
        # Horario
        while True:
            start_time = input("Hora de inicio (HH:MM, 24h): ").strip()
            if InputValidator.validate_time(start_time):
                break
            print("Formato inválido. Use HH:MM (ej: 18:30)")
        
        while True:
            end_time = input("Hora de finalización (HH:MM, 24h): ").strip()
            if InputValidator.validate_time(end_time):
                # Verificar que la hora final sea posterior a la inicial
                try:
                    start_dt = datetime.strptime(start_time, "%H:%M")
                    end_dt = datetime.strptime(end_time, "%H:%M")
                    if end_dt > start_dt:
                        break
                    else:
                        print("La hora final debe ser posterior a la hora inicial")
                except ValueError:
                    print("Horas inválidas")
            else:
                print("Formato inválido. Use HH:MM (ej: 23:00)")
        
        # Número de invitados
        while True:
            num_guests_input = input("Número total de invitados: ").strip()
            if InputValidator.validate_positive_int(num_guests_input):
                num_guests = int(num_guests_input)
                max_guests = 20 * 5  # 20 mesas * 5 personas
                if num_guests <= max_guests:
                    break
                else:
                    print(f"Máximo {max_guests} invitados (20 mesas de 5 personas)")
            else:
                print("Número inválido")
        
        # Calcular mesas automáticamente
        tables_needed = num_guests // 5
        if num_guests % 5 > 0:
            tables_needed += 1
        
        print(f"\nSe necesitarán {tables_needed} mesas para {num_guests} invitados.")
        
        # Seleccionar menú
        print("\nSELECCIÓN DE MENÚ (comida + bebida incluidos):")
        MenuGenerator.display_menu_options()
        
        while True:
            menu_choice = input("\nSeleccione el menú (1-4): ").strip()
            if menu_choice in ["1", "2", "3", "4"]:
                menu = MenuGenerator.get_menu_by_choice(menu_choice)
                break
            print("Opción inválida. Seleccione 1-4")
        
        # Asignar meseros
        print(f"\nASIGNACIÓN DE MESEROS")
        min_waiters_needed = ConstraintChecker.calculate_min_waiters(tables_needed)
        print(f"Se necesitan al menos {min_waiters_needed} mesero(s) (máximo 4 mesas por mesero).")
        
        while True:
            num_waiters_input = input(f"¿Cuántos meseros asignará? (mínimo {min_waiters_needed}): ").strip()
            if InputValidator.validate_positive_int(num_waiters_input):
                num_waiters = int(num_waiters_input)
                if num_waiters >= min_waiters_needed:
                    break
                else:
                    print(f"Necesita al menos {min_waiters_needed} mesero(s)")
            else:
                print("Número inválido")
        
        # Crear IDs de meseros
        waiters_assigned = [f"{wedding_id}_W{i:02d}" for i in range(1, num_waiters + 1)]
        
        # Crear IDs de mesas
        tables_assigned = [f"{wedding_id}_T{i:02d}" for i in range(1, tables_needed + 1)]
        
        # Crear estructura de datos
        wedding_data = {
            "wedding_id": wedding_id,
            "couple_name": couple_name,
            "date": date,
            "start_time": start_time,
            "end_time": end_time,
            "num_guests": num_guests,
            "num_tables": tables_needed,
            "tables_assigned": tables_assigned,
            "waiters_assigned": waiters_assigned,
            "menu_type": menu["name"]
        }
        
        # Verificar conflicto de horario
        if self.db.check_schedule_conflict(wedding_data):
            print("\nError: Hay un conflicto de horario con otra boda en la misma fecha.")
            print("Por favor, revise el calendario de bodas.")
            input("Presione Enter para continuar...")
            return
        
        # Verificar restricciones
        errors = ConstraintChecker.check_wedding_constraints(wedding_data)
        
        if errors:
            print("\nErrores encontrados:")
            for error in errors:
                print(f"  • {error}")
            print("\nNo se puede crear la boda con estos errores.")
        else:
            # Guardar boda
            if self.db.add_wedding(wedding_data):
                print(f"\n¡Boda {wedding_id} creada exitosamente!")
                print(f"Resumen: {couple_name} - {date} {start_time}-{end_time}")
                print(f"Mesas: {tables_needed} | Meseros: {num_waiters} | Menú: {menu['name']}")
            else:
                print("\nError al guardar la boda.")
        
        input("\nPresione Enter para continuar...")
    
    def view_all_weddings(self):
        """Muestra todas las bodas de manera resumida"""
        self.clear_screen()
        self.display_header()
        print("\nTODAS LAS BODAS PROGRAMADAS\n")
        
        weddings = self.db.get_all_weddings()
        
        if not weddings:
            print("No hay bodas registradas.")
        else:
            print(f"{'ID':<8} {'Pareja':<25} {'Fecha':<12} {'Horario':<13} {'Invitados':<10} {'Mesas':<6} {'Meseros':<7} {'Menú'}")
            print("-" * 90)
            
            for wedding in weddings:
                print(f"{wedding['wedding_id']:<8} "
                      f"{wedding['couple_name'][:24]:<25} "
                      f"{wedding['date']:<12} "
                      f"{wedding['start_time']}-{wedding['end_time']:<13} "
                      f"{wedding['num_guests']:<10} "
                      f"{wedding['num_tables']:<6} "
                      f"{len(wedding['waiters_assigned']):<7} "
                      f"{wedding.get('menu_type', 'No asignado')}")
        
        input("\nPresione Enter para continuar...")
    
    def view_wedding_details(self):
        """Muestra detalles específicos de una boda"""
        self.clear_screen()
        self.display_header()
        print("\nDETALLES DE BODA\n")
        
        wedding_id = input("Ingrese el ID de la boda: ").strip().upper()
        wedding = self.db.get_wedding(wedding_id)
        
        if not wedding:
            print(f"\nNo se encontró ninguna boda con ID {wedding_id}")
        else:
            print(f"\n{'='*50}")
            print(f"BODA: {wedding['wedding_id']}")
            print(f"{'='*50}")
            print(f"Pareja: {wedding['couple_name']}")
            print(f"Fecha: {wedding['date']}")
            print(f"Horario: {wedding['start_time']} - {wedding['end_time']}")
            print(f"Invitados: {wedding['num_guests']} personas")
            print(f"Mesas necesarias: {wedding['num_tables']} mesas")
            print(f"Meseros asignados: {len(wedding['waiters_assigned'])}")
            print(f"Menú: {wedding.get('menu_type', 'No asignado')}")
            
            print(f"\nMesas asignadas ({len(wedding['tables_assigned'])}):")
            tables = wedding['tables_assigned']
            for i in range(0, len(tables), 5):
                print("  " + ", ".join(tables[i:i+5]))
            
            print(f"\nMeseros asignados ({len(wedding['waiters_assigned'])}):")
            waiters = wedding['waiters_assigned']
            for i in range(0, len(waiters), 5):
                print("  " + ", ".join(waiters[i:i+5]))
            
            # Mostrar distribución sugerida de mesas por mesero
            print(f"\nDistribución sugerida de mesas:")
            num_tables = wedding['num_tables']
            num_waiters = len(waiters)
            
            # Calcular distribución equitativa
            base_tables_per_waiter = num_tables // num_waiters
            extra_tables = num_tables % num_waiters
            
            for i, waiter_id in enumerate(waiters):
                tables_for_this_waiter = base_tables_per_waiter
                if i < extra_tables:
                    tables_for_this_waiter += 1
                
                # Mostrar mesas específicas para este mesero
                start_idx = sum([base_tables_per_waiter + (1 if j < extra_tables else 0) for j in range(i)])
                end_idx = start_idx + tables_for_this_waiter
                assigned_tables = tables[start_idx:end_idx]
                
                print(f"  {waiter_id}: {tables_for_this_waiter} mesas → {', '.join(assigned_tables)}")
        
        input("\nPresione Enter para continuar...")
    
    def delete_wedding(self):
        """Elimina una boda"""
        self.clear_screen()
        self.display_header()
        print("\nELIMINAR BODA\n")
        
        wedding_id = input("Ingrese el ID de la boda a eliminar: ").strip().upper()
        wedding = self.db.get_wedding(wedding_id)
        
        if not wedding:
            print(f"\nNo se encontró ninguna boda con ID {wedding_id}")
        else:
            print(f"\nBoda encontrada:")
            print(f"  ID: {wedding['wedding_id']}")
            print(f"  Pareja: {wedding['couple_name']}")
            print(f"  Fecha: {wedding['date']}")
            
            confirm = input(f"\n¿Está seguro de eliminar esta boda? (s/n): ").strip().lower()
            
            if confirm == 's':
                if self.db.delete_wedding(wedding_id):
                    print(f"\nBoda {wedding_id} eliminada exitosamente.")
                else:
                    print(f"\nError al eliminar la boda {wedding_id}.")
            else:
                print("\nOperación cancelada.")
        
        input("\nPresione Enter para continuar...")
    
    def check_constraints(self):
        """Verifica restricciones para todas las bodas"""
        self.clear_screen()
        self.display_header()
        print("\nVERIFICACIÓN DE RESTRICCIONES\n")
        
        weddings = self.db.get_all_weddings()
        
        if not weddings:
            print("No hay bodas registradas para verificar.")
        else:
            all_valid = True
            
            for wedding in weddings:
                errors = ConstraintChecker.check_wedding_constraints(wedding)
                
                if errors:
                    all_valid = False
                    print(f"\n⚠  Boda {wedding['wedding_id']} - {wedding['couple_name']}:")
                    for error in errors:
                        print(f"   • {error}")
                else:
                    print(f"\n✓  Boda {wedding['wedding_id']} - {wedding['couple_name']}: OK")
            
            if all_valid:
                print("\n" + "="*50)
                print("¡TODAS LAS BODAS CUMPLEN CON LAS RESTRICCIONES!")
                print("="*50)
            else:
                print("\n" + "="*50)
                print("ALGUNAS BODAS TIENEN PROBLEMAS QUE DEBEN RESOLVERSE")
                print("="*50)
        
        input("\nPresione Enter para continuar...")

def main():
    """Función principal"""
    app = WeddingPlannerApp()
    
    # Crear directorio de datos si no existe
    os.makedirs("data", exist_ok=True)
    
    # Iniciar aplicación
    try:
        app.main_menu()
    except KeyboardInterrupt:
        print("\n\nAplicación interrumpida por el usuario.")
        sys.exit(0)

if __name__ == "__main__":
    main()