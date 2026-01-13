import dearpygui.dearpygui as dpg
from src.data import Data
from src.filedata import filedata
def extraer_callback(sender, app_data):
    inventario = dpg.get_value("inventario")
    cubiculo = dpg.get_value("cubiculo")
    responsable = dpg.get_value("responsable")
    formato = dpg.get_value("formato")


    formatos = []
    if dpg.get_value("chk_txt"): formatos.append("TXT")
    if dpg.get_value("chk_html"): formatos.append("HTML")
    if dpg.get_value("chk_pdf"): formatos.append("PDF")
    if dpg.get_value("chk_excel"): formatos.append("EXCEL")

    if not formatos:
        dpg.configure_item("error_popup", show=True)
        return

    datos = Data(inventario, cubiculo, responsable).generaldata()
    export = filedata(data=datos)
    for formato in formatos:

        if formato == "TXT":
            export.export_txt()
        elif formato == "HTML":
            export.export_html()
        elif formato == "PDF":
            export.export_pdf()
        elif formato == "EXCEL":
            export.export_excel()

    dpg.configure_item("success_popup", show=True)


def showInterface():
    datos = Data()
    datos = datos.generaldata()

    dpg.create_context()
    dpg.create_viewport(title="Extract Info sys", width=800, height=600)
    dpg.setup_dearpygui()

    # Datos Generales
    with dpg.window(label="Datos Generales", width=380, height=250, pos=(10, 10)):
        for clave, valor in datos.items():
            if clave not in ["Discos", "Interfaces de red"]:
                dpg.add_text(f"{clave}: {valor}")

    # Discos
    with dpg.window(label="Discos", width=380, height=250, pos=(410, 10)):
        for disco, info in datos["Discos"].items():
            dpg.add_text(f"{disco}:")
            if isinstance(info, dict):
                for subclave, subvalor in info.items():
                    dpg.add_text(f"   {subclave}: {subvalor}")
            else:
                dpg.add_text(f"   {info}")


    # Interfaces de Red
    with dpg.window(label="Interfaces de Red", width=780, height=150, pos=(10, 270)):
        for iface, direccion in datos["Interfaces de red"].items():
            dpg.add_text(f"{iface}: {direccion}")


    # Entradas de usuario y exportación
    with dpg.window(label="Generador de Informe", width=780, height=150, pos=(10, 430)):
        dpg.add_input_text(label="Inventario", tag="inventario")
        dpg.add_input_text(label="Cubículo", tag="cubiculo")
        dpg.add_input_text(label="Responsable", tag="responsable")

        dpg.add_text("Selecciona formatos de exportación:")
        with dpg.group(horizontal=True):
            dpg.add_checkbox(label="TXT", tag="chk_txt")
            dpg.add_checkbox(label="HTML", tag="chk_html")
            dpg.add_checkbox(label="PDF", tag="chk_pdf")
            dpg.add_checkbox(label="EXCEL", tag="chk_excel")

        dpg.add_button(label="Extraer", callback=extraer_callback)

        with dpg.window(label="Error", modal=True, show=False, tag="error_popup"):
            dpg.add_text("Debes seleccionar al menos un formato antes de generar el informe.")

        with dpg.window(label="Éxito", modal=True, show=False, tag="success_popup"):
            dpg.add_text("Informe generado correctamente en carpeta Data")


    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()
