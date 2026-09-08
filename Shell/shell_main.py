import os
import time
import utility as util
from Shell import menu_actions as func

isAdminRunning = True

menuOptions = {
    0 : {'message': ' Cerrar Menu', 'action': func.closeAdmin},
    1 : {'message': '[WIP] Ver Procesos', 'action': func.wip},
    2 : {'message': '[WIP] Ver Recursos Compartidos', 'action': func.wip},
    3 : {'message': '[WIP] Ver Memoria', 'action': func.wip},
    4 : {'message': '[WIP] Ver Archivos', 'action': func.wip},
    5 : {'message': '[WIP] Ver Dispositivos', 'action': func.wip},
    6 : {'message': '[WIP] Ver Solicitudes de recursos', 'action': func.wip},
    7 : {'message': '[WIP] Ver Liberación de recursos', 'action': func.wip},
    8 : {'message': '[WIP] Ver Situaciones de espera normal', 'action': func.wip},
    9 : {'message': '[WIP] Ver Situaciones de interbloqueo', 'action': func.wip},
    10 : {'message': '[WIP] Seleccionar Escenario', 'action': func.wip},
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
        #Intentamos ejecutar la acción
        menuOptions[int(userInput)]['action']()
    except:
        # Si es un Input invalido soltamos un mensaje de error
        print("Error, valor ingresado incorrecto")
        time.sleep(util.SHORT_WAIT)
    
    

    