import json
import psutil
from ProcessClass import Proceso

class SimuladorSO:
    def __init__(self):
        self.memoria_total = 0
        self.memoria_disponible = 0
        self.recursos_libres = []
        self.procesos = []
        self.archivos_simulados = {} # <- ¡ESTA ES LA LÍNEA QUE FALTABA!

    def cargar_escenario(self, ruta_archivo):
        try:
            with open(ruta_archivo, 'r') as f:
                datos = json.load(f)
            
            # --- LIMPIEZA DE SISTEMA ---
            self.procesos.clear()
            self.recursos_libres.clear()
            
            self.memoria_total = datos['memoria_total']
            self.memoria_disponible = self.memoria_total
            # Usamos .copy() para no modificar la lista original por accidente
            self.recursos_libres = datos['recursos_disponibles'].copy()
            
            for p in datos['procesos']:
                nuevo_proceso = Proceso(p['pid'], p['memoria'], p['recursos'])
                self.procesos.append(nuevo_proceso)
            
            print(f"\n[+] Escenario '{datos['nombre']}' cargado con éxito.")
            print(f"[+] Memoria total: {self.memoria_total} | Recursos: {self.recursos_libres}")
        except FileNotFoundError:
            print("\n[!] Error: No se encontró el archivo JSON.")

    def ejecutar_simulacion(self):
        print("\n--- AVANZANDO SIMULACIÓN (1 CICLO) ---")
        
        # 1. Asignar memoria a los que apenas van entrando
        for p in self.procesos:
            # CAMBIO: Ahora revisa si está Listo O Esperando
            if p.estado in ["Listo", "Esperando"]: 
                if p.memoria_req <= self.memoria_disponible:
                    self.memoria_disponible -= p.memoria_req
                    p.estado = "Ejecutando"
                    print(f"   [+] {p.pid} obtuvo {p.memoria_req} de RAM. Disponible: {self.memoria_disponible}")
                else:
                    p.estado = "Esperando"
                    print(f"   [!] {p.pid} en ESPERA por falta de memoria.")

        # 2. Los que están Ejecutando o Bloqueados intentan tomar UN recurso a la vez
        for p in self.procesos:
            if p.estado in ["Ejecutando", "Bloqueado"]:
                # Busca el primer recurso que le falte
                for recurso in p.recursos_req:
                    if recurso not in p.recursos_asignados:
                        if recurso in self.recursos_libres:
                            self.recursos_libres.remove(recurso)
                            p.recursos_asignados.append(recurso)
                            p.estado = "Ejecutando"
                            print(f"   [+] {p.pid} se apoderó del recurso '{recurso}'.")
                        else:
                            p.estado = "Bloqueado"
                            print(f"   [ALERTA] {p.pid} BLOQUEADO. El recurso '{recurso}' está en uso.")
                        break
                
        # 3. Terminar los que ya completaron todos sus recursos
        for p in self.procesos:
            if p.estado == "Ejecutando" and len(p.recursos_asignados) == len(p.recursos_req):
                p.estado = "Terminado"
                self.memoria_disponible += p.memoria_req
                for r in p.recursos_asignados:
                    self.recursos_libres.append(r)
                print(f"   [ÉXITO] {p.pid} ha terminado. Memoria y recursos liberados.")

        # 2. Los que están Ejecutando o Bloqueados intentan tomar UN recurso a la vez
        for p in self.procesos:
            if p.estado in ["Ejecutando", "Bloqueado"]:
                # Busca el primer recurso que le falte
                for recurso in p.recursos_req:
                    if recurso not in p.recursos_asignados:
                        if recurso in self.recursos_libres:
                            self.recursos_libres.remove(recurso)
                            p.recursos_asignados.append(recurso)
                            p.estado = "Ejecutando" # Se desbloquea si estaba bloqueado
                            print(f"   [+] {p.pid} se apoderó del recurso '{recurso}'.")
                        else:
                            p.estado = "Bloqueado"
                            print(f"   [ALERTA] {p.pid} BLOQUEADO. El recurso '{recurso}' está en uso.")
                        break # Solo toma 1 recurso por ciclo para dar oportunidad a otros
                
        # 3. Terminar los que ya completaron todos sus recursos
        for p in self.procesos:
            if p.estado == "Ejecutando" and len(p.recursos_asignados) == len(p.recursos_req):
                p.estado = "Terminado"
                self.memoria_disponible += p.memoria_req
                for r in p.recursos_asignados:
                    self.recursos_libres.append(r)
                print(f"   [ÉXITO] {p.pid} ha terminado. Memoria y recursos liberados.")

    def ver_estado_sistema(self):
        print("\n--- ESTADO ACTUAL DEL SISTEMA ---")
        print(f"Memoria Disponible: {self.memoria_disponible} / {self.memoria_total}")
        print(f"Recursos Libres: {self.recursos_libres}")
        print("Procesos:")
        for p in self.procesos:
            print(f"  - {p}")

    def analizar_y_recuperar_interbloqueos(self):
        print("\n--- MÓDULO DE DETECCIÓN DE INTERBLOQUEOS ---")
        
        # Filtramos los procesos que se quedaron atrapados
        bloqueados = [p for p in self.procesos if p.estado == "Bloqueado"]
        
        if not bloqueados:
            print("[+] ESTADO: Sistema sano. No se detectaron interbloqueos.")
            return

        print(f"[!] ALERTA: Se detectaron {len(bloqueados)} proceso(s) en estado Bloqueado.")
        print("\n[*] Analizando las 4 condiciones de interbloqueo:")
        
        # Simulamos el análisis dinámico de las condiciones
        recursos_en_disputa = len(self.recursos_libres) == 0
        print("  1. Exclusión Mutua: [PRESENTE] - Los dispositivos no son compartibles.")
        print("  2. Retención y Espera: [PRESENTE] - Procesos retienen memoria mientras esperan recursos.")
        print("  3. No Expropiación: [PRESENTE] - El SO no arrebata recursos a la fuerza de forma natural.")
        
        if len(bloqueados) > 1 and recursos_en_disputa:
            print("  4. Espera Circular: [PRESENTE] - Los procesos bloqueados dependen de recursos ocupados.")
            print("\n[!] DIAGNÓSTICO: INTERBLOQUEO DETECTADO.")
            
            # --- ESTRATEGIA DE RECUPERACIÓN ---
            print("\n--- INICIANDO ESTRATEGIA DE RECUPERACIÓN ---")
            print("[*] Estrategia elegida: Terminación forzada del proceso más reciente (Ruptura de espera circular).")
            
            # Tomamos al último proceso bloqueado como víctima
            victima = bloqueados[-1] 
            print(f"[!] Abortando proceso {victima.pid}...")
            
            victima.estado = "Terminado (Abortado)"
            
            # Liberamos su memoria
            self.memoria_disponible += victima.memoria_req
            
            # Liberamos sus recursos asignados
            for r in victima.recursos_asignados:
                self.recursos_libres.append(r)
                print(f"  -> Recurso '{r}' liberado.")
                
            victima.recursos_asignados.clear()
            
            print(f"\n[+] SISTEMA RECUPERADO. Memoria actual: {self.memoria_disponible}. Recursos libres: {self.recursos_libres}")
        else:
            print("  4. Espera Circular: [NO PRESENTE] - Es una simple inanición o falta de recursos base.")
    # --- MÓDULO DE ARCHIVOS (4.4) ---
    def operar_archivos(self):
        print("\n--- SISTEMA DE ARCHIVOS ---")
        print("Archivos actuales en el disco virtual:", list(self.archivos_simulados.keys()) if self.archivos_simulados else "Ninguno")
        print("1. Crear archivo")
        print("2. Leer archivo")
        print("3. Eliminar archivo")
        
        op = input("Elige una operación (1/2/3) o presiona Enter para cancelar: ")
        
        if op == "1":
            nombre = input("Nombre del nuevo archivo: ")
            if nombre in self.archivos_simulados:
                print(f"[!] Error: El archivo '{nombre}' ya existe.")
            else:
                self.archivos_simulados[nombre] = "En uso"
                print(f"[+] Archivo '{nombre}' creado exitosamente.")
        elif op == "2":
            nombre = input("Nombre del archivo a leer: ")
            if nombre in self.archivos_simulados:
                print(f"[+] Leyendo '{nombre}'... Operación exitosa.")
            else:
                print(f"[!] Error: El archivo '{nombre}' no existe.")
        elif op == "3":
            nombre = input("Nombre del archivo a eliminar: ")
            if nombre in self.archivos_simulados:
                del self.archivos_simulados[nombre]
                print(f"[+] Archivo '{nombre}' eliminado del sistema.")
            else:
                print(f"[!] Error: El archivo '{nombre}' no existe.")

    # --- MÓDULO DE MONITOREO REAL (4.10) ---
    def monitoreo_psutil(self):
        print("\n--- MONITOREO DEL HARDWARE ---")
        print("[!] Recursos de la computadora física.")
        
        cpu_usage = psutil.cpu_percent(interval=0.5)
        ram = psutil.virtual_memory()
        disco = psutil.disk_usage('/')
        
        print(f"[*] Uso de CPU: {cpu_usage}%")
        print(f"[*] Uso de Memoria RAM: {ram.percent}% ({ram.used // (1024**2)} MB usados)")
        print(f"[*] Uso de Almacenamiento: {disco.percent}% ({disco.free // (1024**3)} GB libres)")
        print(f"[*] Estado de Red: {len(psutil.net_connections())} conexiones activas")
    # --- MÓDULO DE LOGS Y REGISTRO (4.9) ---
    def guardar_y_ver_logs(self):
        print("\n--- GESTIÓN DE REGISTRO DE EVENTOS (LOGS) ---")
        
        # Generamos la captura del estado actual
        log_texto = "--- EVENTO DE SISTEMA REGISTRADO ---\n"
        log_texto += f"Memoria Disponible: {self.memoria_disponible} / {self.memoria_total}\n"
        log_texto += f"Recursos Libres: {self.recursos_libres}\n"
        if not self.procesos:
            log_texto += "Sin procesos cargados.\n"
        else:
            for p in self.procesos:
                log_texto += f"[{p.pid}] {p.estado} - Mem: {p.memoria_req} - Rec: {p.recursos_asignados}\n"
        
        # Guardado automático (la "a" significa append, añade al final sin borrar lo anterior)
        with open("simulacion.log", "a") as f:
            f.write(log_texto + "\n")
            
        print("[+] El estado actual del sistema se ha guardado en 'simulacion.log'.")
        
        print("\nOpciones de Log:")
        print("1. Ver el historial completo")
        print("2. Limpiar el historial (Borrar log)")
        
        op = input("Elige una opción (1/2) o presiona Enter para volver: ")
        
        if op == "1":
            try:
                with open("simulacion.log", "r") as f:
                    print("\n--- INICIO DEL ARCHIVO LOG ---")
                    print(f.read())
                    print("--- FIN DEL ARCHIVO LOG ---")
            except FileNotFoundError:
                print("[!] No hay logs guardados todavía.")
        elif op == "2":
            with open("simulacion.log", "w") as f:
                f.write("")
            print("[+] Archivo 'simulacion.log' limpiado exitosamente.")