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
- Versión: 0.1.0 BETA

> [!IMPORTANT] 
> En macOS, es posible que necesites permisos adicionales para acceder a cierta información del sistema. Asegúrate de otorgar los permisos necesarios en las preferencias del sistema. 

Si se bloquea la ejecución de la aplicación, ya que no está firmada por un desarrollador identificado, pero es sin fines de malware, puedes permitir su ejecución manualmente (puedes analizar el código fuente para mayor seguridad):

    - Ve a preferencias del sistema > Seguridad y privacidad > Privacidad >  Ejecutar de todos modos.

Para ejecutar el programa en MacOSX:
```shell
    ./main
```

## Descarga  

Puedes descargar la última versión del archivo binario aquí: [extrac-info-sys](https://github.com/JohnKun136NVCP/os-infosys/releases/tag/v1.0.0).


Para asegurar la integridad del archivo descargado, verifica su checksum SHA-256.

### Verificación de checksum SHA-256
Después de descargar el archivo binario, puedes verificar su checksum SHA-256 utilizando el siguiente comando en la terminal:

- MacOS:
    ```bash
    shasum -a 256 nombre_del_archivo
    ```
- Windows:
    ```powershell
    Get-FileHash nombre_del_archivo -Algorithm SHA256
    ```
- Linux:
    ```bash
    sha256sum nombre_del_archivo
    ```

Para esta versión puede revisar el siguiente release, [v0.0.2 alpha](https://github.com/JohnKun136NVCP/os-infosys/releases/tag/v0.0.2-alpha)

Compara el valor generado con el siguiente checksum proporcionado:

Linux: `939dacebf457c4ec95a8c9c92cbab61a9e47220db4c7bce3f9a7a20cae2ab578`

MacOS: `6855bef9bab4c60261b46a7559743369e18b8de63198159bf431ef0649624373`

Windows: `961d6785fd095bb34bd5c6bf5787a1fd20ce4497fd4c2ec0909fc1868a744378`

## 🖼️ Recursos
Las imágenes se encuentran en la carpeta `img/`.

## 📄 Licencia
Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.
