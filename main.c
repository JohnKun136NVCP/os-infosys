#include <stdio.h>
#include <string.h>
#include "src/data.h"
#include "src/filedata.h"

int main(int argc, char *argv[]) {
    SystemInfo info = get_system_info();

    strcpy(info.inventario, "");
    strcpy(info.cubiculo, "");
    strcpy(info.responsable, "");
    strcpy(info.desktop, "");

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

    export_txt(&info);

    printf("Registro agregado a inventario.txt correctamente.\n");
    return 0;
}
