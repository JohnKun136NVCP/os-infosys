#include <stdio.h>
#include <string.h>
#include "src/data.h"

int main(int argc, char *argv[]) {
    SystemInfo info = get_system_info();

    // Valores por defecto vacíos
    strcpy(info.inventario, "");
    strcpy(info.cubiculo, "");
    strcpy(info.responsable, "");
    strcpy(info.desktop, "");

    // Procesamos argumentos
    for (int i = 1; i < argc; i++) {
        if (strcmp(argv[i], "-I") == 0 && i+1 < argc) {
            strncpy(info.inventario, argv[i+1], sizeof(info.inventario)-1);
        } else if (strcmp(argv[i], "-C") == 0 && i+1 < argc) {
            strncpy(info.cubiculo, argv[i+1], sizeof(info.cubiculo)-1);
        } else if (strcmp(argv[i], "-R") == 0 && i+1 < argc) {
            strncpy(info.responsable, argv[i+1], sizeof(info.responsable)-1);
        } else if (strcmp(argv[i], "-D") == 0 && i+1 < argc) {
            strncpy(info.desktop, argv[i+1], sizeof(info.desktop)-1);
        }
    }

    // Creamos el archivo inventario.txt
    FILE *f = fopen("inventario.txt", "w");
    if (!f) {
        perror("No se pudo crear inventario.txt");
        return 1;
    }

    // Cabecera
    fprintf(f, "Hostname*IP*MACaddress*RAM*Procesador*Sistema*Responsable*Cubículo*Inventario*Desktop\n");

    // Datos
    fprintf(f, "%s*%s*%s*%s*%s*%s*%s*%s*%s*%s\n",
            info.hostname,
            info.ip,
            info.mac,
            info.ram,
            info.cpu,
            info.sistema,
            info.responsable,
            info.cubiculo,
            info.inventario,
            info.desktop);

    fclose(f);

    printf("Archivo inventario.txt generado correctamente.\n");
    return 0;
}
