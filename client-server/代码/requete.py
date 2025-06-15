# coding:utf-8
import socket
import psycopg2

# Database Information
host = "postgresql-bouhadoun.alwaysdata.net"
port = "5433"
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

host, port = ('', 5433)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen()
print("Le serveur est démarré...")

while True:
    conn, address = server_socket.accept()

    try:
        cur = bd_conn.cursor()

        # Vérifier si l'utilisateur existe
        cur.execute("SELECT * FROM Personne WHERE login = %s AND mot_de_passe = %s", (login.strip(), password.strip()))
        result = cur.fetchall()

        if len(result):
            print("L'utilisateur existe.")
        else:
            print("L'utilisateur n'existe pas ou les identifiants sont incorrects.")

        # 可选的查询用户的电子邮件是否存在于 id_personne 表中
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

bd_conn.close()
