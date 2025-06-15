import psycopg2
import psycopg2.extras
from dotenv import load_dotenv
from os import environ
from database import Database
from datetime import datetime
import socket

def log(message):
    print(message)
    with open('logs.txt', 'a') as logs:
        logs.write(f'{datetime.now().strftime("%H:%M:%S")} : {message}\n')

if __name__ == '__main__':
    # Charger les variables d'environnement de la base de données
    load_dotenv()
    db_host = environ.get('DB_HOST')
    db_name = environ.get('DB_NAME')
    db_username = environ.get('DB_USERNAME')
    db_password = environ.get('DB_PASSWORD')

    try:
        db = Database(db_host, db_name, db_username, db_password)
    except Exception as ex:
        log('Échec de la connexion à la base de données.')
        log(f'Erreur : {ex}')
        exit()
    log('Connexion à la base de données établie avec succès.')

    # Charger les variables d'environnement du socket
    sock_host = environ.get('SOCK_HOST')
    sock_port = int(environ.get('SOCK_PORT', 65432))

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((sock_host, sock_port))
        sock.listen()
    except Exception as ex:
        log('Échec de la création du flux socket.')
        log(f'Erreur : {ex}')
        exit()
    log('Flux socket instancié avec succès.')
    log('En écoute...')

    while True:
        conn, addr = sock.accept()
        log(f'Connecté par {addr}')

        try:
            cur = db.conn.cursor()
            cur.execute("SELECT nom, type_carte FROM Personne JOIN Carte ON Personne.id_carte = Carte.id_carte")
            rows = cur.fetchall()

            for row in rows:
                print(f"Nom: {row[0]}, Type de carte: {row[1]}")

        except psycopg2.Error as e:
            log(f"Erreur lors de la requête : {e}")

        finally:
            cur.close()