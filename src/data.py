import psutil
import datetime
import platform
import getpass
import subprocess

class data:
    def __init__(self, inventario="", cubiculo="", responsable=""):
        self.data = {}
        self.inventario = inventario
        self.cubiculo = cubiculo
        self.responsable = responsable

    # --- Métodos auxiliares para CPU y OS ---
    def __get_cpu_linux(self):
        try:
            result = subprocess.run(["lscpu"], capture_output=True, text=True)
            for line in result.stdout.splitlines():
                if "Model name" in line:
                    return line.split(":")[1].strip()
            # fallback: /proc/cpuinfo
            with open("/proc/cpuinfo") as f:
                for line in f:
                    if "model name" in line.lower():
                        return line.split(":")[1].strip()
        except Exception:
            return "No disponible"

    def __get_os_linux(self):
        try:
            result = subprocess.run(
                ["bash", "-c", "source /etc/os-release && echo $PRETTY_NAME"],
                capture_output=True, text=True
            )
            return result.stdout.strip()
        except Exception:
            return f"{platform.system()} {platform.release()}"

    def __get_cpu_macos(self):
        try:
            result = subprocess.run(
                ["sysctl", "-n", "machdep.cpu.brand_string"],
                capture_output=True, text=True
            )
            return result.stdout.strip()
        except Exception:
            return "No disponible"

    def __get_os_macos(self):
        try:
            version = platform.mac_ver()[0]
            return f"macOS {version}" if version else "macOS"
        except Exception:
            return "macOS"

    # --- Método principal ---
    def generaldata(self) -> dict:
        # Datos externos
        self.data["Inventario"] = self.inventario
        self.data["Cubículo"] = self.cubiculo
        self.data["Responsable"] = self.responsable

        # Datos generales
        self.data["Fecha"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        system = platform.system()
        arch = platform.machine()  # arquitectura: x86_64, arm64, etc.

        if system == "Linux":
            cpu = self.__get_cpu_linux()
            sistema = self.__get_os_linux()
        elif system == "Darwin":  # macOS
            cpu = self.__get_cpu_macos()
            sistema = self.__get_os_macos()
        else:  # Windows u otros
            cpu = platform.processor()
            sistema = f"{platform.system()} {platform.release()}"

        # Agregar arquitectura al procesador
        if cpu and arch:
            cpu = f"{cpu} ({arch})"

        self.data["Sistema operativo"] = sistema
        self.data["Procesador"] = cpu
        self.data["Nombre del equipo"] = platform.node()
        self.data["Nombre del usuario"] = getpass.getuser()

        # Hardware
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

        # Red
        interfaces = {}
        for iface, addrs in psutil.net_if_addrs().items():
            direcciones = [addr.address for addr in addrs if addr.family.name == "AF_INET"]
            if direcciones:
                interfaces[iface] = ", ".join(direcciones)
            else:
                interfaces[iface] = "Sin dirección IP"
        self.data["Interfaces de red"] = interfaces

        return self.data
