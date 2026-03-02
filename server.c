#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#ifdef _WIN32
#include <winsock2.h>
#include <ws2tcpip.h>
#pragma comment(lib, "ws2_32.lib")
#else
#include <sys/socket.h>
#include <netinet/in.h>
#endif
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

#define PORT 8080
#define HOST_DIR "host"
#define BUF_SIZE 8192

void send_response(int client, const char *header, const char *body) {
    char response[BUF_SIZE];
    snprintf(response, sizeof(response), "%s\r\n%s", header, body);
    send(client, response, strlen(response), 0);
}

void serve_file(int client, const char *path, const char *content_type) {
    FILE *fp = fopen(path, "rb");
    if (!fp) {
        send_response(client, "HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n", "<h1>404 Not Found</h1>");
        return;
    }
    char header[256];
    snprintf(header, sizeof(header), "HTTP/1.1 200 OK\r\nContent-Type: %s\r\n\r\n", content_type);
    send(client, header, strlen(header), 0);
    char buf[BUF_SIZE];
    size_t n;
    while ((n = fread(buf, 1, sizeof(buf), fp)) > 0) {
        send(client, buf, n, 0);
    }
    fclose(fp);
}

void serve_php(int client, const char *path) {
    char cmd[512];
    snprintf(cmd, sizeof(cmd), "php %s", path);
    FILE *fp = popen(cmd, "r");
    if (!fp) {
        send_response(client, "HTTP/1.1 500 Internal Server Error\r\nContent-Type: text/html\r\n\r\n", "<h1>PHP Error</h1>");
        return;
    }
    char header[] = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n";
    send(client, header, strlen(header), 0);
    char buf[BUF_SIZE];
    size_t n;
    while ((n = fread(buf, 1, sizeof(buf), fp)) > 0) {
        send(client, buf, n, 0);
    }
    pclose(fp);
}

void handle_client(int client) {
    char buf[BUF_SIZE];
    int n = recv(client, buf, sizeof(buf)-1, 0);
    if (n <= 0) return;
    buf[n] = '\0';
    char method[8], path[256];
    sscanf(buf, "%7s %255s", method, path);
    if (strcmp(method, "GET") != 0) {
        send_response(client, "HTTP/1.1 405 Method Not Allowed\r\nContent-Type: text/html\r\n\r\n", "<h1>405 Method Not Allowed</h1>");
        return;
    }
    char file_path[512];
    snprintf(file_path, sizeof(file_path), "%s%s", HOST_DIR, path);
    if (strstr(path, "..")) {
        send_response(client, "HTTP/1.1 400 Bad Request\r\nContent-Type: text/html\r\n\r\n", "<h1>400 Bad Request</h1>");
        return;
    }
    if (strcmp(path, "/") == 0) {
        snprintf(file_path, sizeof(file_path), "%s/index.html", HOST_DIR);
    }
    // Fallback jika file tidak ditemukan dan tidak ada ekstensi
    int has_ext = strstr(path, ".") != NULL;
    FILE *fp = fopen(file_path, "rb");
    if (!fp && !has_ext && strcmp(path, "/") != 0) {
        // Coba tambahkan .html
        snprintf(file_path, sizeof(file_path), "%s%s.html", HOST_DIR, path);
        fp = fopen(file_path, "rb");
        if (fp) {
            serve_file(client, file_path, "text/html");
            fclose(fp);
            return;
        }
    } else if (fp) {
        fclose(fp);
    }
    if (strstr(path, ".php")) {
        serve_php(client, file_path);
    } else if (strstr(path, ".html")) {
        serve_file(client, file_path, "text/html");
    } else if (strstr(path, ".css")) {
        serve_file(client, file_path, "text/css");
    } else if (strstr(path, ".js")) {
        serve_file(client, file_path, "application/javascript");
    } else {
        serve_file(client, file_path, "application/octet-stream");
    }
}

int main() {
    int server_fd, client_fd;
    struct sockaddr_in addr;
    int opt = 1;
#ifdef _WIN32
    WSADATA wsa;
    if (WSAStartup(MAKEWORD(2,2), &wsa) != 0) {
        printf("WSAStartup failed\n");
        return 1;
    }
#endif
    server_fd = socket(AF_INET, SOCK_STREAM, 0);
#ifdef _WIN32
    setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, (const char*)&opt, sizeof(opt));
#else
    setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));
#endif
    addr.sin_family = AF_INET;
    addr.sin_addr.s_addr = INADDR_ANY;
    addr.sin_port = htons(PORT);
    bind(server_fd, (struct sockaddr*)&addr, sizeof(addr));
    listen(server_fd, 10);
    printf("Serving at http://localhost:%d\n", PORT);
    while (1) {
        socklen_t addrlen = sizeof(addr);
        client_fd = accept(server_fd, (struct sockaddr*)&addr, &addrlen);
        handle_client(client_fd);
#ifdef _WIN32
        closesocket(client_fd);
#else
        close(client_fd);
#endif
    }
#ifdef _WIN32
    closesocket(server_fd);
    WSACleanup();
#else
    close(server_fd);
#endif
    return 0;
}
