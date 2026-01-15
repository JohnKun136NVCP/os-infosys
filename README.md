# Inventario de Computadoras (CLI)

## 📌 Descripción
Este proyecto es una herramienta de línea de comandos desarrollada en C que recopila y muestra información detallada sobre el sistema operativo y el hardware de la computadora en la que se ejecuta. Está diseñado para ser ligero y eficiente, proporcionando datos esenciales sin necesidad de dependencias externas.

## 🛠️ Características 
- Información del sistema operativo: nombre, versión, arquitectura.
- Detalles del hardware: CPU, memoria RAM, almacenamiento.
- Información de red: direcciones IP, estado de las interfaces de red.
- Salida formateada para fácil lectura en la terminal.

## 🚀 Uso
Usa el makefile para compilar el proyecto:

```bash
make
```
Luego, ejecuta el programa generado:

```bash
./osinfosys
```
Como es cli tiene las siguientes opciones:
-I Inventario
-C Cubículo
-R Responsable
-D Escritorio/Laptop

Ejempllo de uso:
```bash
./osinfosys -I "000000" -C "B001"-R "Juan Pérez" -D "Laptop"
```
El resultado se guardará en un archivo de texto llamado `inventario.txt` en el mismo directorio donde se ejecuta el programa.


## 📂 Estructura del Proyecto
- `src/`: Contiene los archivos fuente en C.

## 📄 Archivos Principales
- `main.c`: Punto de entrada del programa.
- `src/data.c`: Funciones para recopilar información del sistema.
- `src/filedata.c`: Funciones para manejar la salida de datos.
- `makefile`: Script para compilar el proyecto.


## Release

El realease de este proyecto se encuentra en [osinfosys Releases](https://github.com/JohnKun136NVCP/os-infosys/releases/tag/v0.0.1-alpha-cli)

## Ejecutable (SHA256)

Linux: ```9e23fb2848e47c94dd1f2730cabaeaccc2c27ef256643e0cdb8454ef2bd56bc6  osinfosys-linux```

Windows: ```5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8  osinfosys-windows.exe```

MacOS: ```0929a6e7c21a2e090c0a73623a4818be0a3139c9dd8118c72f8a31275c66a0e2  osinfosys-macos```



## 📝 Licencia
Este proyecto está bajo la Licencia MIT. Consulta el archivo LICENSE para más detalles.
