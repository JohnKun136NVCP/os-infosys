import os
import sys
import shutil

def resource_path(relative_path: str, export_dir: str = None) -> str:
    """
    Devuelve la ruta absoluta al recurso, compatible con PyInstaller.
    Si se indica export_dir, copia el recurso ahí y devuelve la ruta relativa.
    """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    abs_path = os.path.join(base_path, relative_path)

    if export_dir:
        # Copiar el recurso a la carpeta export_dir
        os.makedirs(export_dir, exist_ok=True)
        dest_path = os.path.join(export_dir, os.path.basename(relative_path))
        shutil.copy(abs_path, dest_path)
        return os.path.basename(dest_path)  # ruta relativa para HTML
    else:
        return abs_path
