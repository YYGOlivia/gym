# coding:utf-8
import socket
import psycopg2

# Database Information
host = "postgresql-bouhadoun.alwaysdata.net"
port = 5432
user = "bouhadoun_test"
password = "lounis2001"
database = "bouhadoun_projet"

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

bd_conn = connexionbd()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    server_socket.bind(('', port))
    server_socket.listen()
    print("Le serveur est démarré...")

    while True:
        conn, address = server_socket.accept()

        try:
            cur = bd_conn.cursor()

            # Your queries here
            login = 'Pierre1234'
            mot_de_passe = 'Pierre@1#2'
            cur.execute("SELECT * FROM Personne WHERE login = %s AND mot_de_passe = %s", (login.strip(), mot_de_passe.strip()))
            result = cur.fetchall()

            if len(result):
                print("L'utilisateur existe.")
            else:
                print("L'utilisateur n'existe pas ou les identifiants sont incorrects.")

            response_email = "Donne-moi l'email de la personne"
            conn.send(response_email.encode())

            personne_email = conn.recv(1024).decode('utf-8')
            print("Email de la personne :", personne_email)

            cur.execute("SELECT * FROM Personne WHERE adress_mail = %s", (personne_email.strip(),))
            result_email = cur.fetchall()

            if len(result_email):
                print("L'email existe dans la table 'Personne'.")
            else:
                print("L'email n'existe pas dans la table 'Personne'.")

        except psycopg2.Error as e:
            print(f"Une erreur s'est produite : {e}")

        finally:
            cur.close()
            conn.close()

except OSError as e:
    print(f"Erreur lors de la création du socket : {e}")

finally:
    bd_conn.close()
    server_socket.close()
