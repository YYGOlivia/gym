# coding:utf-8
import socket
import psycopg2

# Informations de la base de données
bd_host = "postgresql-bali.alwaysdata.net"
bd_port = "5432"
bd_user = "bali"
bd_mdp = "projetbdreseau"
bd_nom = "bali_bdreseau"

# Connexion à la base de données
def connexionbd():
    try:
        conn = psycopg2.connect(
            host=bd_host,
            port=bd_port,
            user=bd_user,
            password=bd_mdp,
            database=bd_nom
        )
        print("Connexion à la base de données réussie.")
        return conn
    except psycopg2.Error as e:
        print(f"Erreur lors de la connexion à la base de données : {e}")
        return None

# Connexion à la base de données en dehors de la boucle
bd_conn = connexionbd()

host, port = ('', 5576)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen()
print("Le serveur est démarré...")

# ... (le reste du code reste inchangé)

while True:
    conn, address = server_socket.accept()

    try:
        print("Un client vient de se connecter")
        data = conn.recv(1024).decode('utf-8')
        if not data:
            break
        print("Client dit :", data)

        # Demander au client si ce courrier est un spam ou pas
        if data.lower() == "un courrier est arrive":
            response = "Est-ce un spam?"
            conn.send(response.encode())

            user_response = conn.recv(1024).decode('utf-8')
            print("Client répond :", user_response)

            # Demander au client le nom et prénom du destinataire
            if user_response.strip().lower() == "non":
                
                cur = bd_conn.cursor()
                
                #demander le nom du destinataire 
                response = "Donne-moi le nom du destinataire"
                conn.send(response.encode())

                #Recevoir le nom du destinataire
                destinataire_nom = conn.recv(1024).decode('utf-8')
                print("Nom du Destinataire :", destinataire_nom)

                #demander le prénom du destinataire 
                response = "Donne-moi le prénom du destinataire"
                conn.send(response.encode())

                #Recevoir le prénom du destinataire
                destinataire_prenom = conn.recv(1024).decode('utf-8')
                print("Prénom du Destinataire :", destinataire_prenom)

                try:
                    cur.execute("SELECT * FROM utilisateur WHERE nom = %s and prenom = %s ", (destinataire_nom.strip(), destinataire_prenom.strip()))
                    result = cur.fetchall()

                    if len(result):
                        print("Ce destinataire existe")
                    else:
                        print("Ce destinataire n'existe pas")

                    # Demander l'email de l'expéditeur
                    response_email = "Donne-moi l'email de l'expéditeur"
                    conn.send(response_email.encode())

                    # Recevoir l'email de l'expediteur
                    expediteur_email = conn.recv(1024).decode('utf-8')
                    print("Email de l'Expéditeur :", expediteur_email)

                    cur.execute("SELECT * FROM expediteur WHERE expediteur_email = %s",(expediteur_email.strip(),))
                    result = cur.fetchall()

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
