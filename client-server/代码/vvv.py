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

host, port = ('', 54336)

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

        if data.lower() == "Welcome!":
            response = "Êtes-vous membre? (oui/non)"
            conn.send(response.encode())

            user_response = conn.recv(1024).decode('utf-8')
            print("Client répond :", user_response)
            conn.send(user_response.encode())  # Send back the response to the client

            if user_response.strip().lower() == "oui":
                cur = bd_conn.cursor()

                response = "Veuillez fournir votre login"
                conn.send(response.encode())
                login = conn.recv(1024).decode('utf-8')
                print("login :", login)
                conn.send(login.encode())  # Send back the login to the client

                response = "Veuillez fournir votre mot de passe"
                conn.send(response.encode())
                mot_de_passe = conn.recv(1024).decode('utf-8')
                print("mot de passe :", mot_de_passe)
                conn.send(mot_de_passe.encode())  # Send back the password to the client

                try:
                    # Execute the SQL query to check login credentials
                    cur.execute("SELECT * FROM Personne WHERE login = %s AND mot_de_passe = %s", (login.strip(), mot_de_passe.strip()))
                    result = cur.fetchall()

                    if len(result):
                        print("L'utilisateur existe.")
                        conn.send("Vous êtes connecté.".encode())
                    else:
                        print("L'utilisateur n'existe pas ou les identifiants sont incorrects.")
                        conn.send("Échec de la connexion. Vérifiez vos identifiants.".encode())

                except psycopg2.Error as e:
                    print(f"Une erreur s'est produite lors de l'interaction avec la base de données : {e}")

    finally:
        if 'conn' in locals() or 'conn' in globals():
            conn.close()

# Close the database connection
bd_conn.close()
