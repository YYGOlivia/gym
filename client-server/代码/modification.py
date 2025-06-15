# coding:utf-8
import socket
import psycopg2

# Informations de la base de données
host = "postgresql-bouhadoun.alwaysdata.net"
port = "5432"
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

# Requêtes SQL : Insérer un nouvel utilisateur
try:
    cur = bd_conn.cursor()

    # Insérer un nouvel utilisateur, Yige YANG, dans la table Personne
    sql_insert_personne = """
    INSERT INTO Personne (id_personne, nom, prenom, sexe, num_telephone, adress_mail, login, mot_de_passe, id_carte)
    VALUES ('A10', 'YANG', 'Yige', 'F', '0123456789', 'yygolivia@gmail.com', 'Yige1234', 'Yige@1#2', NULL);
    """
    cur.execute(sql_insert_personne)

    # Créer une nouvelle carte pour Yige YANG dans la table Carte
    sql_insert_carte = """
    INSERT INTO Carte (id_carte, type_carte, date_achat, date_expiration)
    VALUES ('carteA010', 'Membre', '2023-11-13', '2024-11-13');
    """
    cur.execute(sql_insert_carte)

    # Associer le nouvel utilisateur Yige YANG à sa carte
    sql_update_personne = """
    UPDATE Personne SET id_carte = 'carteA004' WHERE id_personne = 'A4';
    """
    cur.execute(sql_update_personne)

    bd_conn.commit()
    print("Nouvel utilisateur ajouté avec succès.")

except psycopg2.Error as e:
    bd_conn.rollback()
    print(f"Erreur lors de l'ajout du nouvel utilisateur : {e}")

finally:
    if bd_conn:
        bd_conn.close()

