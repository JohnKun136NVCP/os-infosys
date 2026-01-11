import os
import sys

def resource_path(relative_path: str) -> str:
    """
    Devuelve la ruta absoluta al recurso, compatible con PyInstaller.
    Cuando se ejecuta empaquetado, los recursos se copian en una carpeta temporal (_MEIPASS).
    """
    try:
        # Cuando se ejecuta con PyInstaller
        base_path = sys._MEIPASS
    except Exception:
        # Cuando se ejecuta en modo normal (fuentes)
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
