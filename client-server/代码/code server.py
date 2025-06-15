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
            if user_response.strip().lower() == "non":
                response = "Voulez-vous vous inscrire? (oui/non)"
                conn.send(response.encode())

                user_registration_response = conn.recv(1024).decode('utf-8')
                print("Client répond à l'inscription :", user_registration_response)

                if user_registration_response.strip().lower() == "oui":
                    # Demander au client les informations personnelles
                    response = "Veuillez fournir votre information"
                
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
if(len(result)==0):
                        try:
                            # Insérer l'email de l'expediteur dans la table "expediteur"
                            cur.execute("INSERT INTO expediteur (expediteur_email) VALUES (%s) RETURNING expediteur_id",
                                        (expediteur_email.strip(),))
                            id_exp = cur.fetchone()[0]
                            bd_conn.commit()
                            print("Insertion réussie. ID de l'expéditeur:", id_exp)

                            # Demander le téléphone de l'expéditeur
                            response_telephone = "Donne moi le téléphone de l'expéditeur"
                            conn.send(response_telephone.encode())

                            # Recevoir le téléphone de l'expéditeur
                            expediteur_telephone = conn.recv(1024).decode('utf-8')
                            print("Téléphone de l'Expéditeur :", expediteur_telephone)

                            # Insérer le téléphone de l'expediteur dans la table "expediteur"
                            cur.execute("UPDATE expediteur SET expediteur_telephone = %s WHERE expediteur_id = %s",
                                        (expediteur_telephone.strip(), id_exp))
                            bd_conn.commit()
                            print("Insertion du téléphone réussie.")

                            # Demander si l'expediteur est une personne ou une entreprise
                            response_exp = "Est-ce que l'expediteur est une entreprise (oui ou non) ?"
                            conn.send(response_exp.encode())

                            # Recevoir la réponse
                            entreprise = conn.recv(1024).decode('utf-8')
                            print("C'est une entreprise :", entreprise)

                            if entreprise.strip().lower() == 'oui':
                                # Demander le nom de l'entreprise
                                response = "Donne moi le nom de l'entreprise"
                                conn.send(response.encode())

                                # Recevoir le nom de l'entreprise
                                entreprise_nom = conn.recv(1024).decode('utf-8')
                                print("Nom de l'entreprise :", entreprise_nom)

                                # Insérer le nom de l'entreprise dans la table "entreprise"
                                cur.execute("INSERT INTO entreprise (entreprise_id, entreprise_nom) VALUES (%s, %s)",
                                            (id_exp, entreprise_nom.strip()))
                                bd_conn.commit()
                                print("Insertion du nom de l'entreprise réussie.")

                                # Demander la description de l'entreprise
                                response_desc = "Donne moi la description de l'entreprise"
                                conn.send(response_desc.encode())

                                # Recevoir la description de l'entreprise
                                entreprise_desc = conn.recv(1024).decode('utf-8')
                                print("Description de l'entreprise :", entreprise_desc)

                                # Insérer la description de l'entreprise dans la table "entreprise"
                                cur.execute("UPDATE entreprise SET entreprise_description = %s WHERE entreprise_id = %s",
                                            (entreprise_desc.strip(), id_exp))
                                bd_conn.commit()
                                print("Insertion de la description de l'entreprise réussie.")
                            else:
                                # Demander le nom de la personne expéditrice
                                response = "Donne moi le nom de la personne expéditrice"
                                conn.send(response.encode())

                                # Recevoir le nom de la personne expéditrice
                                personne_nom = conn.recv(1024).decode('utf-8')
                                print("Nom de la personne expéditrice :", personne_nom)

                                # Insérer le nom de la personne expéditrice dans la table "personne"
                                cur.execute("INSERT INTO personne (personne_id, personne_nom) VALUES (%s, %s)",
                                            (id_exp, personne_nom.strip()))
                                bd_conn.commit()
                                print("Insertion du nom de la personne expéditrice réussie.")

                                # Demander le prénom de la personne expéditrice
                                response_prenom = "Donne moi le prénom de la personne expéditrice"
                                conn.send(response_prenom.encode())

                                # Recevoir le prénom de la personne expéditrice
                                personne_prenom = conn.recv(1024).decode('utf-8')
                                print("Prénom de la personne expéditrice :", personne_prenom)

                                # Insérer le prénom de la personne expéditrice dans la table "personne"
                                cur.execute("UPDATE personne SET personne_prenom = %s WHERE personne_id = %s",
                                            (personne_prenom.strip(), id_exp))
                                bd_conn.commit()
                                print("Insertion du prénom de la personne expéditrice réussie.")

                        except psycopg2.Error as e:
                            bd_conn.rollback()
                            print(f"Erreur lors de l'insertion : {e}")

                finally:
                    # Fermer le curseur après avoir traité toutes les requêtes pour cette connexion
                    cur.close()

    except Exception as e:
        print(f"Une erreur s'est produite : {e}")

    finally:
        # Fermer la connexion après avoir traité un client
        conn.close()

# Fermer la connexion à la base de données après avoir traité tous les clients
bd_conn.close()


def inserer_utilisateur():
    bd_conn = connexionbd()
    if bd_conn:
        try:
            cur = bd_conn.cursor()

            # Insérer un nouvel utilisateur
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
            cur.close()
            bd_conn.close()

# Exécuter la vérification de l'utilisateur
verifier_utilisateur()

# Exécuter l'insertion d'un nouvel utilisateur
inserer_utilisateur()
