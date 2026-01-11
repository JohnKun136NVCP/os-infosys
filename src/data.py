import psutil
import datetime
import platform
import getpass
class data:
    def __init__(self,inventario="",cubiculo="",responsable=""):
        self.data = {}
        self.inventario = inventario
        self.cubiculo = cubiculo
        self.resposable = responsable
    def generaldata(self) ->dict:
        # Datos externos
        self.data["Inventario"] = self.inventario
        self.data["Cubículo"] = self.cubiculo
        self.data["Responsable"] = self.resposable
        #Datos generales
        self.data["Fecha"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.data["Sistema operativo"] = platform.system()
        self.data["Versión OS"] = platform.version()
        self.data["Arquitectura"] = platform.architecture()[0]
        self.data["Procesador"] = platform.processor()
        self.data["Nombre del equipo"] = platform.node()
        self.data["Nombre del usuario"] = getpass.getuser()
        #Hardware
        self.data["CPU Núcleos"] = psutil.cpu_count(logical=False)
        self.data["CPU Hilos"] = psutil.cpu_count(logical=True)
        self.data["Uso CPU(%)"] = psutil.cpu_percent(interval=1)
        self.data["Memoria total (GB)"] = round(psutil.virtual_memory().total / (1024**3), 2)
        disks = {}
        total_size = 0
        for part in psutil.disk_partitions():
            try:
                uso = psutil.disk_usage(part.mountpoint)
                disks[part.device] = {
                    "Punto de montaje": part.mountpoint,
                    "Sistema de archivos": part.fstype,
                    "Total (GB)": round(uso.total / (1024**3), 2),
                    "Usado (GB)": round(uso.used / (1024**3), 2),
                    "Libre (GB)": round(uso.free / (1024**3), 2),
                    "Porcentaje (%)": uso.percent
                }
                total_size += uso.total
            except PermissionError:
                disks[part.device] = {"Error": "No se pudo acceder"}
        disks["Volumen total (GB)"] = round(total_size / (1024**3), 2)
        self.data["Discos"] = disks
        #Red
        interfaces = {}
        for iface, addrs in psutil.net_if_addrs().items():
            direcciones = [addr.address for addr in addrs if addr.family.name == "AF_INET"]
            if direcciones:
                interfaces[iface] = ", ".join(direcciones)
            else:
                interfaces[iface] = "Sin dirección IP"
        self.data["Interfaces de red"] = interfaces

        return self.data
