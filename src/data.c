#include "data.h"
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/utsname.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

#ifdef __linux__
#include <ifaddrs.h>
#include <netpacket/packet.h>   // AF_PACKET
#endif

#ifdef __APPLE__
#include <ifaddrs.h>
#include <net/if_dl.h>
#include <sys/sysctl.h>
#endif

#ifdef _WIN32
#include <windows.h>
#include <iphlpapi.h>
#pragma comment(lib, "iphlpapi.lib")
#endif

SystemInfo get_system_info() {
    SystemInfo info;
    memset(&info, 0, sizeof(SystemInfo));

    // Hostname
    gethostname(info.hostname, sizeof(info.hostname));

    // --- IP y MAC ---
#if defined(__linux__)
    struct ifaddrs *ifaddr, *ifa;
    if (getifaddrs(&ifaddr) == 0) {
        for (ifa = ifaddr; ifa != NULL; ifa = ifa->ifa_next) {
            if (ifa->ifa_addr && ifa->ifa_addr->sa_family == AF_INET) {
                struct sockaddr_in *sa = (struct sockaddr_in *)ifa->ifa_addr;
                if (strcmp(ifa->ifa_name, "lo") != 0) {
                    strncpy(info.ip, inet_ntoa(sa->sin_addr), sizeof(info.ip)-1);
                }
            }
            if (ifa->ifa_addr && ifa->ifa_addr->sa_family == AF_PACKET) {
                struct sockaddr_ll *s = (struct sockaddr_ll*)ifa->ifa_addr;
                if (s->sll_halen >= 6) {
                    snprintf(info.mac, sizeof(info.mac),
                             "%02x:%02x:%02x:%02x:%02x:%02x",
                             s->sll_addr[0], s->sll_addr[1], s->sll_addr[2],
                             s->sll_addr[3], s->sll_addr[4], s->sll_addr[5]);
                }
            }
        }
        freeifaddrs(ifaddr);
    }

#elif defined(__APPLE__)
    struct ifaddrs *ifaddr, *ifa;
    if (getifaddrs(&ifaddr) == 0) {
        for (ifa = ifaddr; ifa != NULL; ifa = ifa->ifa_next) {
            if (ifa->ifa_addr && ifa->ifa_addr->sa_family == AF_INET) {
                struct sockaddr_in *sa = (struct sockaddr_in *)ifa->ifa_addr;
                if (strcmp(ifa->ifa_name, "lo0") != 0) {
                    strncpy(info.ip, inet_ntoa(sa->sin_addr), sizeof(info.ip)-1);
                }
            }
            if (ifa->ifa_addr && ifa->ifa_addr->sa_family == AF_LINK) {
                struct sockaddr_dl* sdl = (struct sockaddr_dl*)ifa->ifa_addr;
                unsigned char *mac = (unsigned char*)LLADDR(sdl);
                if (sdl->sdl_alen >= 6) {
                    snprintf(info.mac, sizeof(info.mac),
                             "%02x:%02x:%02x:%02x:%02x:%02x",
                             mac[0], mac[1], mac[2], mac[3], mac[4], mac[5]);
                }
            }
        }
        freeifaddrs(ifaddr);
    }

#elif defined(_WIN32)
    IP_ADAPTER_INFO AdapterInfo[16];
    DWORD buflen = sizeof(AdapterInfo);
    if (GetAdaptersInfo(AdapterInfo, &buflen) == NO_ERROR) {
        PIP_ADAPTER_INFO pAdapterInfo = AdapterInfo;
        snprintf(info.mac, sizeof(info.mac),
                 "%02X:%02X:%02X:%02X:%02X:%02X",
                 pAdapterInfo->Address[0], pAdapterInfo->Address[1],
                 pAdapterInfo->Address[2], pAdapterInfo->Address[3],
                 pAdapterInfo->Address[4], pAdapterInfo->Address[5]);
        strncpy(info.ip, pAdapterInfo->IpAddressList.IpAddress.String, sizeof(info.ip)-1);
    }
#endif

    // --- RAM total ---
#if defined(__linux__)
    FILE *meminfo = fopen("/proc/meminfo", "r");
    if (meminfo) {
        char line[256];
        while (fgets(line, sizeof(line), meminfo)) {
            if (strncmp(line, "MemTotal:", 9) == 0) {
                long kb = atol(line + 9);
                double gb = (double)kb / (1024.0 * 1024.0);
                if (gb >= 1.0) {
                    snprintf(info.ram, sizeof(info.ram), "%.2f GB", gb);
                } else {
                    double mb = (double)kb / 1024.0;
                    if (mb >= 1.0) {
                        snprintf(info.ram, sizeof(info.ram), "%.2f MB", mb);
                    } else {
                        snprintf(info.ram, sizeof(info.ram), "%ld KB", kb);
                    }
                }
                break;
            }
        }
        fclose(meminfo);
    }

#elif defined(__APPLE__)
    int64_t memsize;
    size_t memsize_len = sizeof(memsize);
    if (sysctlbyname("hw.memsize", &memsize, &memsize_len, NULL, 0) == 0) {
        double gb = (double)memsize / (1024.0 * 1024.0 * 1024.0);
        if (gb >= 1.0) {
            snprintf(info.ram, sizeof(info.ram), "%.2f GB", gb);
        } else {
            double mb = (double)memsize / (1024.0 * 1024.0);
            if (mb >= 1.0) {
                snprintf(info.ram, sizeof(info.ram), "%.2f MB", mb);
            } else {
                snprintf(info.ram, sizeof(info.ram), "%lld KB", memsize / 1024);
            }
        }
    }

#elif defined(_WIN32)
    MEMORYSTATUSEX statex;
    statex.dwLength = sizeof(statex);
    if (GlobalMemoryStatusEx(&statex)) {
        double gb = (double)statex.ullTotalPhys / (1024.0 * 1024.0 * 1024.0);
        if (gb >= 1.0) {
            snprintf(info.ram, sizeof(info.ram), "%.2f GB", gb);
        } else {
            double mb = (double)statex.ullTotalPhys / (1024.0 * 1024.0);
            if (mb >= 1.0) {
                snprintf(info.ram, sizeof(info.ram), "%.2f MB", mb);
            } else {
                snprintf(info.ram, sizeof(info.ram), "%llu KB", statex.ullTotalPhys / 1024);
            }
        }
    }
#endif

    // --- CPU ---
#if defined(__linux__)
    FILE *cpuinfo = fopen("/proc/cpuinfo", "r");
    if (cpuinfo) {
        char line[256];
        while (fgets(line, sizeof(line), cpuinfo)) {
            if (strstr(line, "model name")) {
                char *colon = strchr(line, ':');
                if (colon) {
                    char *val = colon + 1;
                    while (*val == ' ' || *val == '\t') val++;
                    strncpy(info.cpu, val, sizeof(info.cpu)-1);
                    info.cpu[strcspn(info.cpu, "\n")] = 0;
                }
                break;
            }
        }
        fclose(cpuinfo);
    }

#elif defined(__APPLE__)
    size_t cpu_len = sizeof(info.cpu);
    sysctlbyname("machdep.cpu.brand_string", info.cpu, &cpu_len, NULL, 0);

#elif defined(_WIN32)
    HKEY hKey;
    if (RegOpenKeyEx(HKEY_LOCAL_MACHINE,
        "HARDWARE\\DESCRIPTION\\System\\CentralProcessor\\0",
        0, KEY_READ, &hKey) == ERROR_SUCCESS) {
        DWORD dwType = REG_SZ;
        DWORD dwSize = sizeof(info.cpu);
        RegQueryValueEx(hKey, "ProcessorNameString", NULL, &dwType, (LPBYTE)info.cpu, &dwSize);
        RegCloseKey(hKey);
    }
#endif

    // --- Sistema operativo ---
#if defined(__linux__)
    FILE *osrel = fopen("/etc/os-release", "r");
    if (osrel) {
        char line[256];
        while (fgets(line, sizeof(line), osrel)) {
            if (strncmp(line, "PRETTY_NAME=", 12) == 0) {
                char *val = strchr(line, '=');
                if (val) {
                    val++;
                    size_t n = strcspn(val, "\n");
                    val[n] = 0;
                    if (val[0] == '\"') {
                        val++;
                        char *endq = strrchr(val, '\"');
                        if (endq) *endq = 0;
                    }
                    strncpy(info.sistema, val, sizeof(info.sistema)-1);
                }
                break;
            }
        }
        fclose(osrel);
    }

#elif defined(__APPLE__)
    struct utsname unameData;
    if (uname(&unameData) == 0) {
        snprintf(info.sistema, sizeof(info.sistema), "macOS %s", unameData.release);
    } else {
        strncpy(info.sistema, "macOS", sizeof(info.sistema)-1);
    }

#elif defined(_WIN32)
    OSVERSIONINFOEX ver;
    ZeroMemory(&ver, sizeof(ver));
    ver.dwOSVersionInfoSize = sizeof(ver);
    if (GetVersionEx((OSVERSIONINFO*)&ver)) {
        const char *name = "Windows";
        if (ver.dwMajorVersion == 6 && ver.dwMinorVersion == 0) name = "Windows Vista";
        else if (ver.dwMajorVersion == 6 && ver.dwMinorVersion == 1) name = "Windows 7";
        else if (ver.dwMajorVersion == 6 && ver.dwMinorVersion == 2) name = "Windows 8";
        else if (ver.dwMajorVersion == 6 && ver.dwMinorVersion == 3) name = "Windows 8.1";
        else if (ver.dwMajorVersion == 10 && ver.dwMinorVersion == 0) {
            // Windows 10 y Windows 11 comparten 10.0, diferenciación real requiere otra API
            // Aquí asumimos Windows 10/11
            name = "Windows 10/11";
        }
        snprintf(info.sistema, sizeof(info.sistema), "%s (v%lu.%lu)", 
                 name, ver.dwMajorVersion, ver.dwMinorVersion);
    } else {
        strncpy(info.sistema, "Windows", sizeof(info.sistema)-1);
    }
#endif

    return info;
}

