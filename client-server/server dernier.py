import socket
import psycopg2

# Database Information
host = "postgresql-bouhadoun.alwaysdata.net"
port = "5432"
user = "bouhadoun_test"
password = "lounis2001"
database = "bouhadoun_projet"

# Database Connection
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

# Database Connection outside the loop
bd_conn = connexionbd()

host, port = ('', 64555)

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

        # Demander au client s'il est membre de la salle de sport
        if data.lower() == "Welcome!":
            response = "est-ce que vous êtes une membre?(oui/non)"
            conn.send(response.encode())

            user_response = conn.recv(1024).decode('utf-8')
            print("Client répond :", user_response)

            # Demander au client le login et mot de passe
            if user_response.strip().lower() == "oui":
                
                cur = bd_conn.cursor()

            response = "Veuillez fournir votre login"
            conn.send(response.encode())
            login = conn.recv(1024).decode('utf-8')
            print("login :", login)

            response = "Veuillez fournir votre mot de passe"
            conn.send(response.encode())
            mot_de_passe = conn.recv(1024).decode('utf-8')
            print("mot de passe :", mot_de_passe)

            try:
                cur.execute("SELECT * FROM Personne WHERE login = %s AND mot_de_passe = %s", (login.strip(), mot_de_passe.strip()))
                result = cur.fetchall()

                if len(result):
                    print("L'utilisateur existe.")
                else:
                    print("L'utilisateur n'existe pas ou les identifiants sont incorrects.")


            '''# Demander au client s'il souhaite s'inscrire
            if user_response.strip().lower() == "non":
                response = "Voulez-vous vous inscrire? (oui/non)"
                conn.send(response.encode())

                user_registration_response = conn.recv(1024).decode('utf-8')
                print("Client répond à l'inscription :", user_registration_response)

                if user_registration_response.strip().lower() == "oui":
                    response = "Veuillez fournir votre nom"
                    conn.send(response.encode())
                    nom = conn.recv(1024).decode('utf-8')

                    response = "Veuillez fournir votre prénom"
                    conn.send(response.encode())
                    prenom = conn.recv(1024).decode('utf-8')

                    response = "Veuillez fournir votre sexe (F/M)"
                    conn.send(response.encode())
                    sexe = conn.recv(1024).decode('utf-8')

                    response = "Veuillez fournir votre numéro de téléphone"
                    conn.send(response.encode())
                    num_telephone = conn.recv(1024).decode('utf-8')

                    response = "Veuillez fournir votre adresse email"
                    conn.send(response.encode())
                    adress_mail = conn.recv(1024).decode('utf-8')

                    response = "Veuillez fournir votre login"
                    conn.send(response.encode())
                    login = conn.recv(1024).decode('utf-8')

                    response = "Veuillez fournir votre mot de passe"
                    conn.send(response.encode())
                    mot_de_passe = conn.recv(1024).decode('utf-8')

                    cur = bd_conn.cursor()
                    sql_insert_personne = """
                        INSERT INTO Personne (nom, prénom, sexe, num_téléphone, adress_mail, login, mot_de_passe)
                        VALUES (%s, %s, %s, %s, %s, %s, %s);
                    """
                    cur.execute(sql_insert_personne, (nom.strip(), prenom.strip(), sexe.strip(), num_telephone.strip(), adress_mail.strip(), login.strip(), mot_de_passe.strip()))
                    bd_conn.commit()
                    print("Utilisateur inscrit avec succès.")
                else:
                    print("L'utilisateur a choisi de ne pas s'inscrire.")'''
            #else:
                
    except psycopg2.Error as e:
        print(f"Une erreur s'est produite lors de l'interaction avec la base de données : {e}")

    finally:
        # Fermer la connexion après avoir traité un client
        if 'conn' in locals() or 'conn' in globals():
            conn.close()

# # Fermer la connexion à la base de données
bd_conn.close()
