import psycopg2
import psycopg2.extras
from dotenv import load_dotenv
from os import environ
from datetime import datetime
import socket

class Database:
    def __init__(self, host, database, username, password):
        self.connection = psycopg2.connect(
            host=host,
            database=database,
            user=username,
            password=password
        )
        self.cursor = self.connection.cursor()

    def execute(self, query, params=None):
        self.cursor.execute(query, params)
        self.connection.commit()

    def fetchone(self):
        return self.cursor.fetchone()

    def close(self):
        self.cursor.close()
        self.connection.close()


def log(message):
    print(message)
    with open('logs.txt', 'a') as logs:
        logs.write(f'{datetime.now().strftime("%H:%M:%S")} : {message}\n')


def get_person_info_by_id(person_id):
    try:
        # Exécution de la requête SQL
        db.execute("SELECT * FROM Personne WHERE id_personne = %s;", (person_id,))
        result = db.fetchone()

        if result:
            # Extraction des colonnes de la table
            (
                id_personne, nom, prénom, sexe, num_téléphone, adress_mail,
                login, mot_de_passe, id_carte
            ) = result

            # Enregistrement du log avec l'ID de la personne
            log(f"Personne trouvee avec succes. ID Personne : {id_personne}")

            # Filtrer les personnes en fonction de l'identifiant
            if person_id.startswith('A'):
                print("Ce personnage est un client.")
            elif person_id.startswith(('B', 'C', 'D')):
                print("Ce personnage est un employe.")
            else:
                print("Ce personnage n'est ni un client ni un employe.")

            # Affichage des informations
            print("ID Personne:", id_personne)
            print("Nom:", nom)
            print("Prénom:", prénom)
            print("Sexe:", sexe)
            print("Numéro de téléphone:", num_téléphone)
            print("Adresse e-mail:", adress_mail)
            print("Login:", login)
            print("Mot de passe:", mot_de_passe)
            print("ID Carte:", id_carte)

            # Retourner les informations si nécessaire
            return result
        else:
            print("Aucune personne trouvee avec cet ID.")
            return None
    except Exception as ex:
        log(f'Erreur lors de la recuperation des informations de la personne : {ex}')


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

    # Dialogue avec l'utilisateur
    person_id = input("Veuillez entrer l'ID de la personne : ")
    get_person_info_by_id(person_id)