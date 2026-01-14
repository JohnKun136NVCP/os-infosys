import os

class filedata:
    def __init__(self, data: dict):
        self.data = data
        self.__filename = "inventario.txt"
        self.__header = ("Hostname", "IP", "MACaddress", "RAM", "Procesador", 
                         "Sistema", "Responsable", "Cubículo", "Inventario","Desktop")
        self.__new_file = not os.path.exists(self.__filename)

    def export_txt(self) -> None:
        with open(self.__filename, "a") as f:
            if self.__new_file:
                f.write("*".join(self.__header) + "\n")
                f.write("-" * 70 + "\n")  
                self.__new_file = False
            row = [self.data.get(h, "N/A") for h in self.__header]
            f.write("*".join(row) + "\n")
