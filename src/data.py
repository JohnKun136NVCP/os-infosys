import psutil
import socket
import uuid
import platform
import subprocess

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

    def get_system_info(self) -> dict:
        hostname = socket.gethostname()
        ip = self.__get_ip()
        mac = ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff)
                        for ele in range(0,8*6,8)][::-1])
        ram_gb = round(psutil.virtual_memory().total / (1024**3), 2)

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

        return {
            "Hostname": hostname,
            "IP": ip,
            "MACaddress": mac,
            "RAM": f"{ram_gb} GB",
            "Procesador": cpu,
            "Sistema": sistema
        }

    def generaldata(self) -> dict:
        self.data = self.get_system_info()
        self.data["Inventario"] = self.inventario
        self.data["Cubículo"] = self.cubiculo
        self.data["Responsable"] = self.responsable
        return self.data
