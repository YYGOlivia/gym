#include <stdio.h>
#include <winsock2.h>
#pragma comment(lib, "ws2_32.lib")


int main() {
    WSADATA wsa;
    if (WSAStartup(MAKEWORD(2, 2), &wsa) != 0) {
        perror("Erreur lors de l'initialisation de Winsock");
        return 1;
    }

    SOCKET client_socket;
    struct sockaddr_in server_addr;
    char buffer[1024];

    if ((client_socket = socket(AF_INET, SOCK_STREAM, 0)) == INVALID_SOCKET) {
        perror("Erreur lors de la création du socket");
        return 1;
    }

    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(64555);
    server_addr.sin_addr.s_addr = inet_addr("127.0.0.1");

    if (connect(client_socket, (struct sockaddr*)&server_addr, sizeof(server_addr)) == SOCKET_ERROR) {
        perror("Erreur lors de la connexion au serveur");
        closesocket(client_socket);
        WSACleanup();
        return 1;
    }

    // Envoyer un message au serveur
    char message[] = "Bienvenue!";
    send(client_socket, message, strlen(message), 0);

    // Recevoir la demande du serveur
    recv(client_socket, buffer, sizeof(buffer), 0);
    printf("Serveur dit : %s\n", buffer);

    // Lire la réponse de l'utilisateur
    printf("Votre reponse (oui ou non) : ");
    fgets(buffer, sizeof(buffer), stdin);
    send(client_socket, buffer, strlen(buffer), 0);

    // Assurez-vous que la réponse est correcte avant de poursuivre
    if (strcmp(buffer, "oui\n") == 0) {
        // Demande du serveur du nom du destinataire
        recv(client_socket, buffer, sizeof(buffer), 0);
        printf("Serveur dit : %s\n", buffer);
        // Demande du serveur du login
        recv(client_socket, buffer, sizeof(buffer), 0);
        printf("Serveur dit : %s\n", buffer);

        // Envoyer le login
        printf("login: ");
        fgets(buffer, sizeof(buffer), stdin);
        send(client_socket, buffer, strlen(buffer), 0);

        // Demande du serveur du mot de passe
        recv(client_socket, buffer, sizeof(buffer), 0);
        printf("Serveur dit : %s\n", buffer);

        // Envoyer le prénom de la personne expéditrice
        printf("mot-de-passe: ");
        fgets(buffer, sizeof(buffer), stdin);
        send(client_socket, buffer, strlen(buffer), 0);

         // Lire la réponse de l'utilisateur
       '''printf("oui ou non : ");
       fgets(buffer, sizeof(buffer), stdin);
       send(client_socket, buffer, strlen(buffer), 0);

        if (strcmp(buffer, "oui\n") == 0) {
        // Demande du serveur du nom du destinataire
        recv(client_socket, buffer, sizeof(buffer), 0);
        printf("Serveur dit : %s\n", buffer);
        

        printf("nom: ");
        fgets(buffer, sizeof(buffer), stdin);
        send(client_socket, buffer, strlen(buffer), 0);
        recv(client_socket, buffer, sizeof(buffer), 0);
        printf("Serveur dit : %s\n", buffer);

        printf("prénom: ");
        fgets(buffer, sizeof(buffer), stdin);
        send(client_socket, buffer, strlen(buffer), 0);
        recv(client_socket, buffer, sizeof(buffer), 0);
        printf("Serveur dit : %s\n", buffer);

        printf("sexe: ");
        fgets(buffer, sizeof(buffer), stdin);
        send(client_socket, buffer, strlen(buffer), 0);
        recv(client_socket, buffer, sizeof(buffer), 0);
        printf("Serveur dit : %s\n", buffer);

        printf("numéro de téléphone: ");
        fgets(buffer, sizeof(buffer), stdin);
        send(client_socket, buffer, strlen(buffer), 0);
        recv(client_socket, buffer, sizeof(buffer), 0);
        printf("Serveur dit : %s\n", buffer);

        printf("email: ");
        fgets(buffer, sizeof(buffer), stdin);
        send(client_socket, buffer, strlen(buffer), 0);
        recv(client_socket, buffer, sizeof(buffer), 0);
        printf("Serveur dit : %s\n", buffer);

        printf("login: ");
        fgets(buffer, sizeof(buffer), stdin);
        send(client_socket, buffer, strlen(buffer), 0);
        recv(client_socket, buffer, sizeof(buffer), 0);
        printf("Serveur dit : %s\n", buffer);
    

         printf("mot de passe: ");
        fgets(buffer, sizeof(buffer), stdin);
        send(client_socket, buffer, strlen(buffer), 0);
        recv(client_socket, buffer, sizeof(buffer), 0);
        printf("Serveur dit : %s\n", buffer);'''


        
           
        }
    } else {
        printf("Réponse non valide. Quitter.\n");
    }

        
    closesocket(client_socket);
    WSACleanup();

    return 0;
}
