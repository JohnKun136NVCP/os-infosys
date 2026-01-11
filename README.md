# Inventario de Computadoras

## 📌 Descripción
Este programa permite extraer información del sistema (hardware, discos, interfaces de red, etc.) y exportarla en distintos formatos (TXT, HTML, PDF, Excel).

## 🚀 Uso
1. Crea un entorno virtual:
   ```bash
   python -m venv venv
   ```
2. Activa el entorno virtual:
    - En Windows:
        ```bash
        .\venv\Scripts\activate
        ```
    - En Linux/macOS:
        ```bash
        source venv/bin/activate
        ```
3. Instala las dependencias:
    ```bash
    pip install -r requirements.txt
    ```
4. Ejecuta `main.py` en tu entorno virtual.
5. Llena los campos de inventario, cubículo y responsable.
6. Selecciona los formatos de exportación.
7. Haz clic en **Extraer**.

## 📦 Exportación
Los informes se guardan en la carpeta `Data/`.
 
## Disponible en
- Windows
- Linux
- macOS

## 👤 Autor
- Nombre: JohnKun136NVCP
- Versión: 1.0.0

> [!IMPORTANT] 
> En macOS, es posible que necesites permisos adicionales para acceder a cierta información del sistema. Asegúrate de otorgar los permisos necesarios en las preferencias del sistema. 

Si se bloquea la ejecución de la aplicación, ya que no está firmada por un desarrollador identificado, pero es sin fines de malware, puedes permitir su ejecución manualmente (puedes analizar el código fuente para mayor seguridad):

    - Ve a preferencias del sistema > Seguridad y privacidad > Privacidad >  Ejecutar de todos modos.

Para ejecutar el programa en MacOSX:
```shell
    ./main
```


## 🖼️ Recursos
Las imágenes se encuentran en la carpeta `img/`.

## 📄 Licencia
Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.