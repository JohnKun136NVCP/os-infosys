import os
import re
import polars as pl
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from src.utils import resource_path
class filedata:
    def __init__(self,data:dict):
        self.data = data
        self.basename = ""
    def __sanitize_filename(self,name: str) -> str:
        # Reemplaza caracteres inválidos por guiones bajos
        return re.sub(r'[<>:"/\\|?*]', '_', name)
    def __basenameData(self,type:str) ->str:
        fecha = self.__sanitize_filename(self.data.get("Fecha", ""))
        nombre = self.__sanitize_filename(self.data.get("Nombre del equipo", ""))
        inventario = self.__sanitize_filename(self.data.get("Inventario", ""))
        self.basename = f"{nombre}_{inventario}_{fecha}"+f".{type}"
        return self.basename
    def __dataDirExists(self):
        os.makedirs("Data",exist_ok=True)
    def export_txt(self) ->None:
        self.__dataDirExists()
        self.__basenameData('txt')
        filename = os.path.join("Data", self.basename)
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"=== INFORME DE COMPUTADORA  {self.data["Nombre del equipo"]}===\n\n")
            for clave, valor in self.data.items():
                if isinstance(valor, dict):
                    f.write(f"{clave}:\n")
                    for subclave, subvalor in valor.items():
                        f.write(f"  {subclave}: {subvalor}\n")
                else:
                    f.write(f"{clave}: {valor}\n")
    def export_html(self,img1="..img/img1.png", img2="..img/img2.png") -> None:
        self.__dataDirExists()
        self.__basenameData('html')
        img1 = resource_path("img/img1.png")
        img2 = resource_path("img/img2.png")
        filename = os.path.join("Data", self.basename)
        with open(filename, "w", encoding="utf-8") as f:
            f.write("""
            <html>
            <head>
                <meta charset="UTF-8">
                <title>Informe de Computadora</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 40px; background-color: #f9f9f9; }
                    h1 { text-align: center; color: #2c3e50; }
                    h2 { text-align: center; color: #34495e; }
                    .header { text-align: center; margin-bottom: 20px; }
                    .header img { height: 80px; margin: 10px; }
                    ul { list-style-type: none; padding: 0; }
                    li { margin: 5px 0; }
                    .section { margin-top: 20px; }
                </style>
            </head>
            <body>
                <div class="header">
                    <img src='""" + img1 + """' alt='Logo 1'>
                    <img src='""" + img2 + """' alt='Logo 2'>
                </div>
                <h1>INFORME COMPUTADORA """ + self.data["Nombre del equipo"] + """</h1>
                <h2>Fecha: """ + self.data["Fecha"] + """</h2>
                <div class="section">
                    <ul>
            """)
            for k, v in self.data.items():
                if isinstance(v, dict):
                    f.write(f"<li><strong>{k}:</strong><ul>")
                    for subclave, subvalor in v.items():
                        f.write(f"<li>{subclave}: {subvalor}</li>")
                    f.write("</ul></li>")
                else:
                    f.write(f"<li><strong>{k}:</strong> {v}</li>")
            f.write("""
                    </ul>
                </div>
            </body>
            </html>
            """)
    def export_pdf(self):
        self.__dataDirExists()
        self.__basenameData('pdf')
        filename = os.path.join("Data", self.basename)
        c = canvas.Canvas(filename, pagesize=letter)
        width, height = letter

        # Título y subtítulo (centrados)
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(width/2, height-100, f"INFORME COMPUTADORA {self.data["Nombre del equipo"]}")
        c.setFont("Helvetica", 12)
        c.drawCentredString(width/2, height-120, f"Fecha: {self.data['Fecha']}")

        # Contenido
        y = height-160
        c.setFont("Helvetica", 10)
        for clave, valor in self.data.items():
            if isinstance(valor, dict):
                c.drawString(50, y, f"{clave}:")
                y -= 15
                for subclave, subvalor in valor.items():
                    c.drawString(70, y, f"{subclave}: {subvalor}")
                    y -= 15
            else:
                c.drawString(50, y, f"{clave}: {valor}")
                y -= 15

            # Si se acaba la página, crear nueva
            if y < 50:
                c.showPage()
                c.setFont("Helvetica", 10)
                y = height-50

        c.save()
    def export_excel(self):
        self.__dataDirExists()
        self.__basenameData('xlsx')
        filename = os.path.join("Data", self.basename)
        filas = []
        for clave, valor in self.data.items():
            if isinstance(valor, dict):
                for subclave, subvalor in valor.items():
                    filas.append({"Categoria": clave, "Campo": subclave, "Valor": str(subvalor)})
            else:
                filas.append({"Categoria": "General", "Campo": clave, "Valor": str(valor)})
        df = pl.DataFrame(filas)
        df.write_excel(filename)
