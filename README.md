# Wedding-Scheduler

## Resumen

Sistema de planificación de bodas para agencia con capacidad limitada.

## Características

- Gestión completa de bodas con horarios y fechas
- Sistema de mesas con capacidad de 5 invitados máximo
- Asignación de meseros (máximo 4 mesas por mesero)
- Menús predefinidos (comida + bebida)
- Verificación de restricciones (constraints)
- Prevención de conflictos de horario
- Base de datos en JSON

## Modelo de Datos:

- Wedding: Información de la boda (pareja, fecha, horario)
- Table: Mesas con menú y asignación de mesero
- Waiter: Meseros con mesas asignadas

## Restricciones Implementadas

1. **Capacidad de mesas**: Máximo 5 invitados por mesa
2. **Meseros**: Máximo 4 mesas asignadas por mesero
3. **Mesas totales**: Máximo 20 mesas disponibles
4. **Menú**: Cada mesa debe tener comida + bebida asignada
5. **Horarios**: No puede haber conflictos entre bodas

## Instalación y Ejecución

1. Aségurese de que Python 3.x esté instalado en su sistema
2. Clone o descargue los archivos del proyecto
3. Ejecute la aplicación 'python main.py' o 'python3 main.py'

## Uso

## Menú Principal

- **Crear nueva boda**: Crea una nueva boda
  - Ingresar un ID para indentificar la boda en el sistema
  - Ingresar el nombre de la pareja
  - Determinar la fecha a la que la boda tendrá lugar
  - Definir hora de inicio y final de la boda
  - Definir cantidad de invitados
  - Determinar el tipo de menú que se servirá
  - Determinar la cantidad de meseros que servirán en la boda
- **Ver bodas existentes**: Muestra una lista con todas las bodas en cola
- **Gestionar boda específica**: Muestra información detallada de una boda en específico
- **Verificar restricciones**: Verifica que todas las bodas cumplan con las restricciones establecidas

## Manejo de Datos

- Los datos se cargan automáticamente desde database.json al inicio
- Los cambios se guardan de manera automática después de operaciones exitosas
- Si database.json no existe, la aplicación crea un nuevo archivo vacío para comenzar a guardar datos

## Implementación Técnica

**Lenguaje**: Python 3
**Interfaz**: Aplicación de Consola
**Manejo de Tiempo**: Módulo 'datetime' para manejo dinámico del tiempo
**Almacenamiento** Formato JSON para persistencia
**Estructura Modular**:
- 'src/': Carpeta que contiene todo el código fuente del proyecto
  - 'constraints/': Carpeta que contiene la verificación de restricciones
    - 'checker.py': Clase constraint, que verifica restricciones en una boda
  - 'data/': Persistencia de datos
    - 'database.py': Archivo que trabaja con la persistencia de datos del proyecto
  - 'models/': Carpeta de modelos
    - 'boda.py': Clase boda
    - 'mesa.py': Clase mesa
    - 'mesero.py: Clase mesero
  - 'utils/': Carpeta con archivos útiles
    - 'helpers.py': Carpeta con ayuda adicional al crear una boda
- 'data/': Datos persistentes
  - 'data.json': Archivo de datos
- 'main.py': Script de punto de entrada del proyecto

## Manejo de Errores

La aplicación muestra mensajes de error claros para:
- Formatos de fecha/hora inválidos
- Conflictos de horarios entre bodas
- Violaciones de restricciones
- Problemas de cargas de archivos

## Licencia

Este proyecto es para fines educativos y académicos

## NOTAS

Si eres estudiante y estás leyendo esto, siéntete libre de tomar ideas si algo te parece interesante, pero no simplemente copies y pegues, sé creativo a tu propia manera.

## COPYRIGHT: Alejandra Suárez Socorro C121
