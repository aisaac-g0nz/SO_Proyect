import time
import sys
import os # ¡Asegúrate de agregar este import!
import Utility as util

from OperativeSystem import SimuladorSO 

mi_so = SimuladorSO()

def cerrar_menu():
    print("\nApagando el sistema de forma segura...")
    time.sleep(util.SHORT_WAIT)
    os._exit(0) # Esto aniquila el proceso instantáneamente, ignorando los 'except'

# --- NUEVA FUNCIÓN DINÁMICA ---
def elegir_escenario():
    print("\n--- Elegir Escenario ---")
    carpeta = "escenarios"
    
    # Verificamos si la carpeta existe
    if not os.path.exists(carpeta):
        print(f"[!] Error: No se encontró la carpeta '{carpeta}'.")
        input("\nPresiona Enter para continuar...")
        return

    # Filtramos solo los archivos .json
    archivos = [f for f in os.listdir(carpeta) if f.endswith('.json')]
    
    if not archivos:
        print("[!] No hay archivos JSON en la carpeta 'escenarios'.")
        input("\nPresiona Enter para continuar...")
        return

    # Imprimimos la lista con índices
    print("Escenarios disponibles:")
    for i, archivo in enumerate(archivos):
        print(f" [{i + 1}] {archivo}")
        
    # Leemos la opción del usuario
    try:
        opcion = int(input("\nSelecciona el número de escenario: "))
        if 1 <= opcion <= len(archivos):
            archivo_seleccionado = archivos[opcion - 1]
            ruta = os.path.join(carpeta, archivo_seleccionado)
            # Llamamos al SO con la ruta dinámica
            mi_so.cargar_escenario(ruta)
        else:
            print("[!] Opción fuera de rango.")
    except ValueError:
        print("[!] Por favor ingresa un número válido.")
        
    input("\nPresiona Enter para continuar...")

# ... (El resto de tus funciones: correr_simulacion, ver_estado_general, etc. se quedan igual) ...

def correr_simulacion():
    # Este es el "Modo Automático" que pide el PDF
    mi_so.ejecutar_simulacion()
    input("\nPresiona Enter para continuar...")

def ver_estado_general():
    # Esto te salva varios puntos de la rúbrica (Ver memoria, recursos y procesos)
    mi_so.ver_estado_sistema()
    input("\nPresiona Enter para continuar...")

def en_construccion():
    print("\n[!] Función no implementada por falta de tiempo (¡Ups!).")
    input("\nPresiona Enter para continuar...")

def accion_router():
    # Función de respaldo por si algo falla en tu ShellMain.py
    pass

def modulo_interbloqueos():
    mi_so.analizar_y_recuperar_interbloqueos()
    input("\nPresiona Enter para continuar...")

def modulo_archivos():
    mi_so.operar_archivos()
    input("\nPresiona Enter para continuar...")

def modulo_monitoreo():
    mi_so.monitoreo_psutil()
    input("\nPresiona Enter para continuar...")

def modulo_logs():
    mi_so.guardar_y_ver_logs()
    input("\nPresiona Enter para continuar...")