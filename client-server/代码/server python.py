import socket

def main():
    port_serveur = 64554

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serveur_socket:
            serveur_socket.bind(('', port_serveur))
            serveur_socket.listen(1)
            print("En attente de la connexion du client...")
                                          
            while True:
                client_socket, addr = serveur_socket.accept()
                print("Connexion du client réussie : ", addr)

                lecteur = client_socket.makefile('r')
                ecrivain = client_socket.makefile('w')

                message = lecteur.readline()
                print("Message reçu du client :", message)

                reponse = "Bonjour depuis le serveur Python"
                ecrivain.write(reponse + '\n')
                ecrivain.flush()
                print("Réponse envoyée au client :", reponse)

                lecteur.close()
                ecrivain.close()
                client_socket.close()

    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()


