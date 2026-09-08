class Proceso:
    def __init__(self, pid, memoria_req, recursos_req):
        self.pid = pid
        self.memoria_req = memoria_req
        self.recursos_req = recursos_req
        self.recursos_asignados = []
        self.estado = "Listo" # Estados: Listo, Esperando, Bloqueado, Terminado

    def __str__(self):
        return f"[{self.pid}] Estado: {self.estado} | Mem: {self.memoria_req} | Recursos: {self.recursos_req}"