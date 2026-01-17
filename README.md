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

## Ejecutable (SHA256) para 64 bits

Linux: ```9e23fb2848e47c94dd1f2730cabaeaccc2c27ef256643e0cdb8454ef2bd56bc6  osinfosys-linux```

Windows: ```5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8  osinfosys-windows.exe```

MacOS: ```a6098d19964149690147e34bcdc58c65eee104c660271e85d32fe90e18fb6844  osinfosys-macos```


## Ejecutable para 32 bits

Linux: ```7ec0721976ead274fab4617afa98c394b811b30aff71a0de77685cc6d510c50a  osinfosys-linux-32```

Windows: ```66a546c041d1f0717a1c0908cd7073291ec6287123a466df45f0d9b6e1d92edc  osinfosys-windows-32.exe```


> [!NOTE]  
> En versión de MacOS menore a mojave (10.14) el ejecutable se debe ejecutar desde terminal.

## Compilación para 32 bits en MacOS

 ```bash
 clang -m32 main.c src/data.c src/filedata.c -I src -o osinfosys-macos-32
 ```

 ### Notas extras

Dejaré la compilación por si alguien lo quiere hacer manualmente.

Para 64 bits en Linux:

```bash
    gcc main.c src/data.c src/filedata.c -I src -o osinfosys-linux
```

 Para 64 bits en Windows (usando MinGW):

```bash
    gcc main.c src/data.c src/filedata.c -I src -o osinfosys-windows.exe -lws2_32 -liphlpapi
    
```

Para 64 bits en MacOS:

```bash
    clang main.c src/data.c src/filedata.c -I src -o osinfosys-macos
```


 En versiones de 32 bits, en Linux:

[!NOTE]
> Previamente se debe descargar las librerías de 32 bits en la distribución que se esté usando.

Ejemplo en Ubuntu/Debian:

```bash
    sudo apt-get install gcc-multilib g++-multilib libc6-dev-i386
```    


```bash
    gcc -m32 main.c src/data.c src/filedata.c -I src -o osinfosys-linux-32
```

Para Windows de 32 bits (usando MinGW) usando MSYS2:

[!NOTE]
> Previamente se debe descargar las librerías de 32 bits en MSYS2.
> Además de ejecutar el siguiente comando en la terminal de MSYS2:

```bash
    pacman -S mingw-w64-i686-gcc # Instalar compilador de 32 bits
    pacman -S mingw-w64-ucrt-x86_64-gcc # Instalar compilador de 64 bits
```

Además de ello agregar la ruta del compilador de 32 bits a la variable de entorno PATH.

Finalmente compilar con el siguiente comando:

```bash
   i686-w64-mingw32-gcc main.c src/data.c src/filedata.c -I src -o osinfosys-windows-32.exe -lws2_32 -liphlpapi
```



## 📝 Licencia
Este proyecto está bajo la Licencia MIT. Consulta el archivo LICENSE para más detalles.
