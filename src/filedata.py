import os

class filedata:
    def __init__(self, data: dict):
        self.data = data
        self.__filename = "inventario.txt"
        self.__col_widths = [15, 15, 20, 10, 40, 20, 20, 12, 12]  
        self.__header = ("Hostname", "IP", "MACaddress", "RAM", "Procesador", 
                         "Sistema", "Responsable", "Cubículo", "Inventario")
        self.__new_file = not os.path.exists(self.__filename)

    def export_txt(self) -> None:
        with open(self.__filename, "a") as f:
            if self.__new_file:
                # Escribir encabezado con formato
                f.write("".join(f"{h:<{w}}" for h, w in zip(self.__header, self.__col_widths)) + "\n")
                f.write("-" * sum(self.__col_widths) + "\n")
                self.__new_file = False  # ya existe después de la primera escritura

            # Ordenar los datos según el encabezado
            row = [self.data.get(h, "N/A") for h in self.__header]

            # Escribir registro con formato
            f.write("".join(f"{d:<{w}}" for d, w in zip(row, self.__col_widths)) + "\n")
            f.write("-" * sum(self.__col_widths) + "\n")
