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
    server_addr.sin_port = htons(5576);
    server_addr.sin_addr.s_addr = inet_addr("127.0.0.1");

    if (connect(client_socket, (struct sockaddr*)&server_addr, sizeof(server_addr)) == SOCKET_ERROR) {
        perror("Erreur lors de la connexion au serveur");
        closesocket(client_socket);
        WSACleanup();
        return 1;
    }

    // Envoyer un message au serveur
    char message[] = "Un courrier est arrive";
    send(client_socket, message, strlen(message), 0);

    // Recevoir la demande du serveur
    recv(client_socket, buffer, sizeof(buffer), 0);
    printf("Serveur dit : %s\n", buffer);

    // Lire la réponse de l'utilisateur
    printf("Votre réponse (oui ou non) : ");
    fgets(buffer, sizeof(buffer), stdin);
    send(client_socket, buffer, strlen(buffer), 0);

    // Assurez-vous que la réponse est correcte avant de poursuivre
    if (strcmp(buffer, "non\n") == 0) {
        // Demande du serveur du nom du destinataire
        recv(client_socket, buffer, sizeof(buffer), 0);
        printf("Serveur dit : %s\n", buffer);

        // Envoyer le nom du destinataire
        printf("Nom Destinataire: ");
        fgets(buffer, sizeof(buffer), stdin);
        send(client_socket, buffer, strlen(buffer), 0);

        // Demande du serveur du prénom du destinataire
        recv(client_socket, buffer, sizeof(buffer), 0);
        printf("Serveur dit : %s\n", buffer);

        // Envoyer le prénom du destinataire
        printf("Prénom Destinataire: ");
        fgets(buffer, sizeof(buffer), stdin);
        send(client_socket, buffer, strlen(buffer), 0);

        // Demande du serveur de l'email de l'expéditeur
        recv(client_socket, buffer, sizeof(buffer), 0);
        printf("Serveur dit : %s\n", buffer);

        // Envoyer l'email de l'expéditeur
        printf("Email de l'expéditeur: ");
        fgets(buffer, sizeof(buffer), stdin);
        send(client_socket, buffer, strlen(buffer), 0);

        // Demande du serveur du téléphone de l'expéditeur
        recv(client_socket, buffer, sizeof(buffer), 0);
        printf("Serveur dit : %s\n", buffer);

        // Envoyer le téléphone de l'expéditeur
        printf("Téléphone de l'expéditeur: ");
        fgets(buffer, sizeof(buffer), stdin);
        send(client_socket, buffer, strlen(buffer), 0);

        // Demande du serveur si l'expéditeur est une entreprise
        recv(client_socket, buffer, sizeof(buffer), 0);
        printf("Serveur dit : %s\n", buffer);

        // Envoyer la réponse sur le statut de l'expéditeur (entreprise ou non)
        printf("Réponse (oui ou non) : ");
        fgets(buffer, sizeof(buffer), stdin);
        send(client_socket, buffer, strlen(buffer), 0);

        if (strcmp(buffer, "oui\n") == 0) {
            // Demande du serveur du nom de l'entreprise
            recv(client_socket, buffer, sizeof(buffer), 0);
            printf("Serveur dit : %s\n", buffer);

            // Envoyer le nom de l'entreprise
            printf("Nom de l'entreprise: ");
            fgets(buffer, sizeof(buffer), stdin);
            send(client_socket, buffer, strlen(buffer), 0);

            // Demande du serveur de la description de l'entreprise
            recv(client_socket, buffer, sizeof(buffer), 0);
            printf("Serveur dit : %s\n", buffer);

            // Envoyer la description de l'entreprise
            printf("Description de l'entreprise: ");
            fgets(buffer, sizeof(buffer), stdin);
            send(client_socket, buffer, strlen(buffer), 0);
        } else {
            // Demande du serveur du nom de la personne expéditrice
            recv(client_socket, buffer, sizeof(buffer), 0);
            printf("Serveur dit : %s\n", buffer);

            // Envoyer le nom de la personne expéditrice
            printf("Nom de la personne expéditrice: ");
            fgets(buffer, sizeof(buffer), stdin);
            send(client_socket, buffer, strlen(buffer), 0);

            // Demande du serveur du prénom de la personne expéditrice
            recv(client_socket, buffer, sizeof(buffer), 0);
            printf("Serveur dit : %s\n", buffer);

            // Envoyer le prénom de la personne expéditrice
            printf("Prénom de la personne expéditrice: ");
            fgets(buffer, sizeof(buffer), stdin);
            send(client_socket, buffer, strlen(buffer), 0);
        }
    } else {
        printf("Réponse non valide. Quitter.\n");
    }

    closesocket(client_socket);
    WSACleanup();

    return 0;
}
