import psutil
import socket
import uuid
import platform

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

    def get_system_info(self) -> dict:
        hostname = socket.gethostname()
        ip = self.__get_ip()
        mac = ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff)
                        for ele in range(0,8*6,8)][::-1])
        ram_gb = round(psutil.virtual_memory().total / (1024**3), 2)
        cpu = platform.processor()
        sistema = f"{platform.system()} {platform.release()}"
        
        return {
            "Hostname": hostname,
            "IP": ip,
            "MACaddress": mac,
            "RAM": f"{ram_gb} GB",
            "Procesador": cpu,
            "Sistema": sistema
        }

    def generaldata(self) -> dict:
        # Combinar datos externos con los del sistema
        self.data = self.get_system_info()
        self.data["Inventario"] = self.inventario
        self.data["Cubículo"] = self.cubiculo
        self.data["Responsable"] = self.responsable
        return self.data