# coding:utf-8
import psycopg2

# Informations de la base de données
host = "postgresql-bouhadoun.alwaysdata.net"
port = "5432"
user = "bouhadoun_test"
password = "lounis2001"
database = "bouhadoun_projet"

# Connexion à la base de données
def connexionbd():
    try:
        conn = psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )
        print("Connexion à la base de données réussie.")
        return conn
    except psycopg2.Error as e:
        print(f"Erreur lors de la connexion à la base de données : {e}")
        return None


# Connexion à la base de données en dehors de la boucle
bd_conn = connexionbd()

host, port = ('', 64554)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen()
print("Le serveur est démarré...")

while True:
    conn, address = server_socket.accept()

    try:
        print("Un client vient de se connecter")
        data = conn.recv(1024).decode('utf-8')
        if not data:
            break
        print("Client dit :", data)

        # Demander au client si il/elle est une membre de notre salle de sport
        if data.lower() == "Bienvenue!":
            response = "est-ce que vous être une membre?"
            conn.send(response.encode())

            user_response = conn.recv(1024).decode('utf-8')
            print("Client répond :", user_response)

            # Demander au client le nom et prénom du destinataire
            if user_response.strip().lower() == "oui":
                
                cur = bd_conn.cursor()
                
                #demander le nom d'untilisateur 
                response = "Donne-moi le nom d'untilisateur"
                conn.send(response.encode())

                #Recevoir le nom d'untilisateur
                login = conn.recv(1024).decode('utf-8')
                print("Nom d'untilisateur :", login)

                #demander le mot de passe d'untilisateur
                response = "Donne-moi le mot de passe"
                conn.send(response.encode())

                #Recevoir le mot de passe d'untilisateur
                mot_de_passe = conn.recv(1024).decode('utf-8')
                print("mot de passe :", mot_de_passe)

        try:
            cur.execute("SELECT * FROM Personne WHERE login = %s AND mot_de_passe = %s", (login.strip(), mot_de_passe.strip()))
            result = cur.fetchall()

            if len(result):
                print("L'utilisateur existe.")
            else:
                print("L'utilisateur n'existe pas ou les identifiants sont incorrects.")

        except psycopg2.Error as e:
            print(f"Une erreur s'est produite lors de la vérification de l'utilisateur : {e}")

   
    finally:
        # Fermer la connexion après avoir traité un client
        if 'conn' in locals() or 'conn' in globals():
            conn.close()

# # Fermer la connexion à la base de données
bd_conn.close()
