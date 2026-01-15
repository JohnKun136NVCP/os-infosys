#include "filedata.h"
#include <stdio.h>
#include <stdbool.h>
#include <string.h>

void export_txt(SystemInfo *info) {
    FILE *f;
    bool new_file = false;

   
    f = fopen("inventario.txt", "r");
    if (!f) {
        new_file = true; 
    } else {
        fclose(f);
    }

    f = fopen("inventario.txt", "a");
    if (!f) return;

    if (new_file) {
        fprintf(f, "Hostname*IP*MACaddress*RAM*Procesador*Sistema*Responsable*Cubículo*Inventario*Desktop\n");
    }

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
