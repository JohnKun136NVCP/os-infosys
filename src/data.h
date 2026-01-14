#ifndef DATA_H
#define DATA_H

typedef struct {
    char hostname[128];
    char ip[64];
    char mac[64];
    char ram[64];
    char cpu[128];
    char sistema[128];
    char responsable[128];
    char cubiculo[64];
    char inventario[64];
    char desktop[64];
} SystemInfo;

SystemInfo get_system_info();

#endif
