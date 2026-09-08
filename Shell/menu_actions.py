import time
import Utility as util
from Shell import ShellMain as shell


def wip():
    print("Lo sentimos, está función sigue en desarrollo")
    time.sleep(util.SHORT_WAIT)

def closeAdmin():
    print("Tenga buen día!")
    shell.isAdminRunning = False
    