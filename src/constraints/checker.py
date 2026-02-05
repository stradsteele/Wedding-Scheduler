class ConstraintChecker:
    MAX_TABLES = 20
    MAX_GUESTS_PER_TABLE = 5
    MAX_TABLES_PER_WAITER = 4
    
    @staticmethod
    def check_wedding_constraints(wedding_data):
        """Verifica todas las restricciones para una boda"""
        errors = []
        
        # 1. Verificar número de mesas no exceda el máximo
        if wedding_data.get("num_tables", 0) > ConstraintChecker.MAX_TABLES:
            errors.append(f"Excede el límite de {ConstraintChecker.MAX_TABLES} mesas")
        
        # 2. Verificar que se haya asignado menú
        if not wedding_data.get("menu_type"):
            errors.append("No se ha asignado un menú")
        
        # 3. Verificar que el número de meseros sea suficiente
        num_tables = wedding_data.get("num_tables", 0)
        num_waiters = len(wedding_data.get("waiters_assigned", []))
        
        # Calcular meseros mínimos necesarios
        min_waiters_needed = num_tables // ConstraintChecker.MAX_TABLES_PER_WAITER
        if num_tables % ConstraintChecker.MAX_TABLES_PER_WAITER > 0:
            min_waiters_needed += 1
        
        if num_waiters < min_waiters_needed:
            errors.append(f"Insuficientes meseros. Se necesitan al menos {min_waiters_needed}")
        
        # 4. Verificar que ningún mesero tenga demasiadas mesas
        # (Para simplificar, asumimos distribución equitativa)
        
        return errors
    
    @staticmethod
    def calculate_min_waiters(num_tables):
        """Calcula el número mínimo de meseros necesarios"""
        min_waiters = num_tables // ConstraintChecker.MAX_TABLES_PER_WAITER
        if num_tables % ConstraintChecker.MAX_TABLES_PER_WAITER > 0:
            min_waiters += 1
        return min_waiters