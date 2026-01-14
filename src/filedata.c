#include "filedata.h"
#include <stdio.h>
#include <stdbool.h>
#include <string.h>

void export_txt(SystemInfo *info) {
    FILE *f;
    bool new_file = false;

    // Verificar si el archivo existe
    f = fopen("inventario.txt", "r");
    if (!f) {
        new_file = true; // no existe, hay que crear encabezados
    } else {
        fclose(f);
    }

    // Abrir en modo append
    f = fopen("inventario.txt", "a");
    if (!f) return;

    if (new_file) {
        fprintf(f, "Hostname*IP*MACaddress*RAM*Procesador*Sistema*Responsable*Cubículo*Inventario*Desktop\n");
        fprintf(f, "----------------------------------------------------------------------\n");
    }

    // Si IP o MAC están vacíos, se dejan en blanco pero se mantiene el orden
    const char *ip = (strlen(info->ip) > 0) ? info->ip : "";
    const char *mac = (strlen(info->mac) > 0) ? info->mac : "";

    fprintf(f, "%s*%s*%s*%s*%s*%s*%s*%s*%s*%s\n",
        info->hostname,
        ip,
        mac,
        info->ram,
        info->cpu,
        info->sistema,
        info->responsable,
        info->cubiculo,
        info->inventario,
        info->desktop
    );

    fclose(f);
}
