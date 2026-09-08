import os
import time
import Utility as util
from Shell import menu_actions as func

isAdminRunning = True

menuOptions = {
    0 : {'message': ' Cerrar Simulador', 'action': func.cerrar_menu},
    1 : {'message': ' Elegir Escenario a Cargar', 'action': func.elegir_escenario},
    2 : {'message': ' Ejecutar Simulación (Modo Automático)', 'action': func.correr_simulacion},
    3 : {'message': ' Ver Estado del Sistema (Procesos, Memoria y Recursos)', 'action': func.ver_estado_general},
    4 : {'message': ' Administración de Archivos Similados', 'action': func.modulo_archivos},
    5 : {'message': ' Monitoreo de Hardware Real (psutil)', 'action': func.modulo_monitoreo},
    6 : {'message': ' Registro de Eventos (Guardar/Ver Logs)', 'action': func.modulo_logs},
    7 : {'message': ' Analizar y Resolver Interbloqueos', 'action': func.modulo_interbloqueos},
}

def bootUp():
    os.system('cls')
    print("-- Cargando Sistema Operativo --")
    time.sleep(util.SHORT_WAIT)
    while isAdminRunning:
        showMenu()
        readOptions()


def showMenu():
    message = ''
    for messageIndex in menuOptions:
        messageText = menuOptions[messageIndex]['message']
        message = message+f'[{messageIndex}]{messageText}\n'
    print("--- Administrador ---")
    time.sleep(util.SHORT_WAIT)
    print(message)
    time.sleep(util.SHORT_WAIT)
    print("Esperando Respuesta...")

def readOptions():
    userInput = input()
    time.sleep(util.SHORT_WAIT)
    try:
        # Intentamos ejecutar la acción
        menuOptions[int(userInput)]['action']()
    except Exception as e:
        # AHORA SÍ VEREMOS EL ERROR REAL
        print(f"\n[ERROR CRÍTICO DEL SISTEMA]: {e}")
        time.sleep(util.SHORT_WAIT)
    
    

    