import dearpygui.dearpygui as dpg
from src.data import Data
from src.filedata import filedata

def extraer_callback(sender, app_data):
    inventario = dpg.get_value("inventario") or "N/A"
    cubiculo = dpg.get_value("cubiculo") or "N/A"
    responsable = dpg.get_value("responsable") or "N/A"

    datos = Data(inventario, cubiculo, responsable).generaldata()
    export = filedata(data=datos)

    # Exportar siempre a TXT
    export.export_txt()

    # Mostrar popup de éxito
    dpg.configure_item("success_popup", show=True)


def showInterface():
    datos = Data()
    datos = datos.generaldata()

    dpg.create_context()
    dpg.create_viewport(title="Extract Info sys", width=800, height=600)
    dpg.setup_dearpygui()

    # Ventana izquierda: Datos Generales
    with dpg.window(label="Datos Generales", width=380, height=580, pos=(10, 10)):
        for clave, valor in datos.items():
            if clave not in ["Discos", "Interfaces de red"]:
                dpg.add_text(f"{clave}: {valor}")

    # Ventana derecha: Entradas de usuario y exportación
    with dpg.window(label="Generador de Informe", width=380, height=580, pos=(410, 10)):
        dpg.add_input_text(label="Inventario", tag="inventario")
        dpg.add_input_text(label="Cubículo", tag="cubiculo")
        dpg.add_input_text(label="Responsable", tag="responsable")

        dpg.add_button(label="Extraer", callback=extraer_callback)

        with dpg.window(label="Éxito", modal=True, show=False, tag="success_popup"):
            dpg.add_text("Informe generado correctamente en carpeta Data")

    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()
