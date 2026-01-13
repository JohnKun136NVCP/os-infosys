import psutil
import socket
import uuid
import platform
import subprocess
import datetime
import getpass

class Data:
    def __init__(self, inventario="", cubiculo="", responsable=""):
        self.data = {}
        self.inventario = inventario
        self.cubiculo = cubiculo
        self.responsable = responsable 


    def __get_ip(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception:
            return "No disponible"

    def __get_cpu_linux(self):
        try:
            result = subprocess.run(["lscpu"], capture_output=True, text=True)
            for line in result.stdout.splitlines():
                if "Model name" in line:
                    return line.split(":")[1].strip()
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

    def __get_cpu_windows(self):
        try:
            result = subprocess.run(
                ["wmic", "cpu", "get", "Name"],
                capture_output=True, text=True
            )
            lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]
            if len(lines) > 1:
                return lines[1]
            return platform.processor()
        except Exception:
            try:
                # Respaldo con PowerShell
                result = subprocess.run(
                    ["powershell", "-Command", "Get-CimInstance Win32_Processor | Select-Object -ExpandProperty Name"],
                    capture_output=True, text=True
                )
                return result.stdout.strip() or platform.processor()
            except Exception:
                return platform.processor()


    def get_system_info(self) -> dict:
        hostname = socket.gethostname()
        ip = self.__get_ip()
        mac = ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff)
                        for ele in range(0,8*6,8)][::-1])
        ram_gb = round(psutil.virtual_memory().total / (1024**3), 2)

        system = platform.system()
        arch = platform.machine()

        if system == "Linux":
            cpu = self.__get_cpu_linux()
            sistema = self.__get_os_linux()
        elif system == "Darwin":  # macOS
            cpu = self.__get_cpu_macos()
            sistema = self.__get_os_macos()
        elif system == "Windows":
            cpu = self.__get_cpu_windows()
            sistema = f"{platform.system()} {platform.release()}"
        else:
            cpu = platform.processor()
            sistema = f"{platform.system()} {platform.release()}"

        if cpu and arch:
            cpu = f"{cpu} ({arch})"


        # --- Información extendida ---
        info = {
            "Fecha": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Hostname": hostname,
            "Nombre del equipo": platform.node(),
            "Nombre del usuario": getpass.getuser(),
            "IP": ip,
            "MACaddress": mac,
            "RAM": f"{ram_gb} GB",
            "Procesador": cpu,
            "Sistema": sistema,
            "CPU Núcleos": psutil.cpu_count(logical=False),
            "CPU Hilos": psutil.cpu_count(logical=True),
            "Uso CPU(%)": psutil.cpu_percent(interval=1),
        }

        # Discos
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
        info["Discos"] = disks

        # Interfaces de red
        interfaces = {}
        for iface, addrs in psutil.net_if_addrs().items():
            direcciones = [addr.address for addr in addrs if addr.family.name == "AF_INET"]
            if direcciones:
                interfaces[iface] = ", ".join(direcciones)
            else:
                interfaces[iface] = "Sin dirección IP"
        info["Interfaces de red"] = interfaces

        return info

    def generaldata(self) -> dict:
        self.data = self.get_system_info()
        self.data["Inventario"] = self.inventario
        self.data["Cubículo"] = self.cubiculo
        self.data["Responsable"] = self.responsable
        return self.data
