import psycopg2
import psycopg2.extras
from os import environ
from datetime import datetime
import socket
import re

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





'''PORTIQUE SALLE'''

def verifier_abonnement_actif_by_id_carte(id_carte):
    try:

        # Exécution de la requête SQL pour obtenir les informations de la carte
        db.execute("""
            SELECT id_carte, type_carte, date_achat, date_expiration
            FROM Carte
            WHERE id_carte =  %s;
        """, (id_carte,))
        carte_info = db.fetchone()

        if carte_info:
            
            (id_carte, type_carte, date_achat, date_expiration) = carte_info

          
            log(f"Informations de carte trouvées avec succès pour la personne. ID Carte : {id_carte}")

         
            date_actuelle = datetime.now().date()
           
            if date_expiration is None:
                resultat_abonnement = "Accès autorisé. L'abonnement est actif."
            elif date_actuelle <= date_expiration:
                resultat_abonnement = "Accès autorisé. L'abonnement est actif."
            else:
                resultat_abonnement = "Veuillez recharger votre compte. L'abonnement a expiré."
                db.execute("SELECT * FROM Personne WHERE Personne.id_carte = %s;", (id_carte,))
                personne_info = db.fetchone()

                if personne_info:
               
                    (id_personne, nom, prénom, sexe, num_téléphone, adress_mail,login, mot_de_passe, id_carte ) = personne_info

               
                    log(f"Votre carte correspond à cet utilisateur, ID Personne : {id_personne}, Nom: {nom}, Prénom: {prénom}")
                    log(resultat_abonnement)
                    return "ABONNEMENT EXPIRE OU INVALIDE"

            log(resultat_abonnement)

            # Extraction n°2 des infos de la personne
            db.execute("SELECT * FROM Personne WHERE Personne.id_carte = %s;", (id_carte,))
            personne_info = db.fetchone()

            if personne_info:
                
                (id_personne, nom, prénom, sexe, num_téléphone, adress_mail,login, mot_de_passe, id_carte ) = personne_info

            
                log(f"Votre carte correspond à cet utilisateur, ID Personne : {id_personne}, Nom: {nom}, Prénom: {prénom}")

                return "ABONNEMENT OK"

            else:
                print("Aucune personne trouvee avec cet ID.")
                return ""
        else:
            print("Aucune information de carte trouvée pour cette personne.")
            return "Veuillez recharger votre compte. Aucune information de carte trouvée."

    except Exception as ex:
        log(f'Erreur lors de la vérification de l\'abonnement : {ex}')
        return "Erreur lors de la vérification de l'abonnement."

def get_type_carte(id_carte):
    
    try:

        db.execute("SELECT type_carte FROM Carte WHERE id_carte =  %s;", (id_carte,))
        carte_info = db.fetchone()
        if carte_info:
            type_carte = carte_info[0]
            return type_carte

    except Exception as ex:
        return "Erreur lors de la vérification de l'abonnement."
    
def carte_exist(id_carte):
    
    try:

        db.execute("SELECT * FROM Carte WHERE id_carte =  %s;", (id_carte,))
        carte_info = db.fetchone()
        if carte_info:
            return "TRUE"
        else:
            return "FALSE"

    except Exception as ex:
        return "FALSE"
    

def verif_accees_portique(id_portique):
    try:

        db.execute("SELECT adress_portique, type_portique FROM portique WHERE id_portique = %s;", (id_portique,))
        portique_info = db.fetchone()

        if portique_info:
         
            (adress_portique, type_portique) = portique_info

            
            log(f"Le portique choisi est reservé aux {type_portique}s")

            # Comparaison avec la date actuelle
            type_carte = get_type_carte(data)

            if type_carte == type_portique:
                resultat_portique = "Accès autorisé au portique. "
                log(resultat_portique)
                return "Acces portique autorise"
            else:
                resultat_portique = "Veuillez vous pésenter au bon portique."
                log(resultat_portique)
                return "mauvais portique, ce portique est reservé aux "+type_portique+"s)"


            
        else:
            print("Aucune portique trouve avec cet ID.")
            return ""
    except Exception as ex:
        log(f'Erreur lors de la recuperation des informations de la personne : {ex}')













'''PARKING'''

def verif_est_un_membre(idc):
     
    try:

        db.execute("SELECT type_carte FROM Carte WHERE id_carte =  %s;", (idc,))
        carte_info = db.fetchone()
        if carte_info:
            carte_info = carte_info[0]
            return carte_info

        else : 
            return "carte inexistante"

    except Exception as ex:
        return "Erreur lors de la vérification de la carte."

def verif_abo_premium(idc):
    try:

        tc = verif_est_un_membre(idc)
        if (tc == "Membre"):
            db.execute("SELECT type_abonnement FROM membre WHERE id_membre = (SELECT id_personne FROM personne WHERE id_carte = %s);", (idc,))
            idp = db.fetchone()
            idp = idp[0]
            if (idp == "premium"):
           
                return "ABO OUI"
        
            else:
                return "ABO NON"
        elif (tc == "Employé"):
            return "EMPLOYE"
        else: return ""
            
        

    except Exception as ex:
        return "NON"
    

def verif_parkingexist(idparking):
    try:
        db.execute("SELECT id_parking FROM parking WHERE id_parking = %s;", (idparking,))
        idp = db.fetchone()
        if idp:
           
            return "PARKING OUI"
        
        else:
            return "PARKING NON"
            
        

    except Exception as ex:
        return "NON"
    

def verif_vehi_exist(vehi):
        try:
            db.execute("SELECT type_vehicule FROM vehicule WHERE type_vehicule = %s;", (vehi,))
            tp = db.fetchone()
            if tp:
               
                return "vehicule autorise"
                
            else:
                print("vehicule non atorise")
            
        

        except Exception as ex:
            return "NON"
    




def obtenir_dernier_id_vehicule():
    try:

        db.execute("SELECT 'vehicule' || MAX(CAST(SUBSTRING(id_vehicule FROM 9) AS INTEGER)) AS max_identifiant FROM vehicule WHERE id_vehicule LIKE 'vehicule%';")
        id_vehi = db.fetchone()
        if id_vehi:
            last_id = id_vehi[0]
            return last_id

    except Exception as ex:
        return "Erreur lors de la recherche du dernier ID véhicule."


def gener_id_vehi():
    
    last_id = obtenir_dernier_id_vehicule()
    if last_id:
        # Extraire le nombre de l'ancien id_vehicule
        nombre = int(re.search(r'\d+', last_id).group())
        nouveau_nombre = nombre + 1

        # Générer le nouvel id_vehicule
        nouvel_id = re.sub(r'\d+', str(nouveau_nombre).zfill(len(str(nombre))), last_id)
        return nouvel_id
    else:
        # Si la table est vide, commencer avec le premier id_vehicule
        return 'véhicule1'
    

def maj_cap_max(id_parking):
    try:
        db.execute("SELECT capacite FROM parking WHERE id_parking = %s;", (id_parking,))
        cap = db.fetchone()
        if cap:
            cap = cap[0]
            if(cap-1 >= 0):
                db.execute("UPDATE parking SET capacite = %s WHERE id_parking = %s;", (cap-1, id_parking,))
                resultat_cap = "Capacité suffisante dans "+id_parking+" la capacité est de "+ str(cap - 1)
                log(resultat_cap)
                return cap-1
            else:
                resultat_cap = "Capacité insuffisante dans "+id_parking
                log(resultat_cap)
                return cap
        else:
            log("Aucune parking trouve avec cet ID.")
            return ""


    except Exception as ex:
        return "NON"

def creer_reserv_véhicule(idparking, vehi):

    try:
        db.execute("SELECT id_parking FROM parking WHERE id_parking = %s;", (idparking,))
        idp = db.fetchone()
        if idp:
            new_id = gener_id_vehi()
            res_new_id = "Votre ID de reservation est "+new_id
            log(res_new_id)

            db.execute("INSERT INTO vehicule  (id_vehicule, type_vehicule, id_parking) VALUES (%s, %s, %s);", (new_id, vehi, idparking))
            resultat_reserv = "reservation ok dans "+idparking
            log(resultat_reserv)
            return "RESERVATION PRISE EN COMPTE"
        
        else:
            resultat_reserv = "parking introuvable avec id : "+idparking
            log(resultat_reserv)
        return ""
            
        

    except Exception as ex:
        return "NON"
    







if __name__ == '__main__':
    DB_HOST= "postgresql-bouhadoun.alwaysdata.net"
    DB_PORT= 5432
    DB_USERNAME = "bouhadoun_test"
    DB_PASSWORD= "lounis2001"
    DB_NAME= "bouhadoun_projet"

    try:
        db = Database(DB_HOST, DB_NAME, DB_USERNAME, DB_PASSWORD)
    except Exception as ex:
        log('Échec de la connexion à la base de données.')
        log(f'Erreur : {ex}')
        exit()
    log('Connexion à la base de données établie avec succès.')

    # Charger les variables d'environnement du socket
    sock_host = "localhost"
    sock_port = 65433

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((sock_host, sock_port))
    server_socket.listen(1)
    while True:
        # Afficher le message du serveur en attente de connexion
        print("Serveur en attente de connexion...")
        print("Port :", sock_port)

        client_socket, client_address = server_socket.accept()
        print(f"Connexion établie avec {client_address}")
        client_socket.send('Tapez 1 pour entrer dans la salle, 2 pour reserver une place de parking :\n'.encode('utf-8'))

        try:
           
            client_socket.settimeout(20)
            # Demander à l'utilisateur de choisir entre entrer dans la salle (1) ou réserver une place de parking (2)
            choix_utilisateur = client_socket.recv(1024).decode('utf-8').rstrip('\n').strip()
           

            if choix_utilisateur == '1':
               
                print("En attente de l'id carte...")
                client_socket.send('En attente de l id carte ...\n'.encode('utf-8'))
                data = client_socket.recv(1024).decode('utf-8').rstrip('\n').strip()
                ce = carte_exist(data)
                result2 = verifier_abonnement_actif_by_id_carte(data)
                if (ce == "TRUE"):
                    if (result2 == "ABONNEMENT OK"):
                        client_socket.sendall('Votre carte et votre abonnement sont valides\n'.encode('utf-8'))
                        print("En attente de l'id portique...")
                        client_socket.sendall('En attente de l id portique ...\n'.encode('utf-8'))
                        data2 = client_socket.recv(1024).decode('utf-8').rstrip('\n').strip()
                        result = verif_accees_portique(data2)
                        if (result == "Acces portique autorise"):
                            client_socket.sendall('PORTIQUE OK, BONNE SEANCE !\n'.encode('utf-8'))
                        elif (result == "Aucune portique trouve avec cet ID."):
                            client_socket.sendall('mauvais ID, portique inexistant\n'.encode('utf-8'))
                        else : 
                            client_socket.sendall('Vous vous presentez au mauvais portique\n'.encode('utf-8'))
                    else : 
                        client_socket.sendall('Votre abonnement est invalide\n'.encode('utf-8'))
                else : 
                    client_socket.sendall('Votre carte est inexistante ou est invalide\n'.encode('utf-8'))
                        

            elif choix_utilisateur == '2':
                
                print("En attente de l'id carte...")
                client_socket.sendall('En attente de l id carte ...\n'.encode('utf-8'))
                data = client_socket.recv(1024).decode('utf-8').rstrip('\n').strip()
                carte = (data)
                vc= verif_abo_premium(carte)
                print(vc)
                if (vc == "ABO OUI"):
                    client_socket.sendall('Vous possedez un abonnement premium, poursuite de la reservation\n'.encode('utf-8'))
                    client_socket.sendall('En attente du type de véhicule...\n'.encode('utf-8'))
                    print("En attente du type de vehicule...")
                    data2 = client_socket.recv(1024).decode('utf-8').rstrip('\n').strip()
                    vehi = (data2)
                    vv= verif_vehi_exist(vehi)
                    if (vv == "vehicule autorise"):
                        client_socket.sendall('Votre vehicule est autorise\n'.encode('utf-8'))
                        client_socket.sendall('En attente de l id parking...\n'.encode('utf-8'))
                        print("En attente de l'id parking...")
                        data3 = client_socket.recv(1024).decode('utf-8').rstrip('\n').strip()
                        idparking = (data3)
                        vp=verif_parkingexist(idparking)
                        if(vp == "PARKING OUI"):
                            result2 = maj_cap_max(idparking)
                            if (result2 > 0):
                                result = creer_reserv_véhicule(idparking, vehi)
                                if(result == "RESERVATION PRISE EN COMPTE"):
                                    client_socket.sendall('Votre reservation a bien ete prise en compte\n'.encode('utf-8'))
                                else :
                                    client_socket.sendall('erreur lors de la reservation\n'.encode('utf-8'))
                            else : 
                                client_socket.sendall('Il n y a plus de place dans ce parking\n'.encode('utf-8'))
                        else :
                            client_socket.sendall('ce parking n existe pas\n'.encode('utf-8'))

                    else : 
                        client_socket.sendall('Votre vehicule n est pas autorise sur nos parking\n'.encode('utf-8'))

                elif (vc == "EMPLOYE"):
                    client_socket.sendall('Vous etes un employe, poursuite de la reservation\n'.encode('utf-8'))
                    print("En attente du type de vehicule...")
                    client_socket.sendall('En attente du type de vehicule...\n'.encode('utf-8'))
                    data2 = client_socket.recv(1024).decode('utf-8').rstrip('\n').strip()
                    vehi = (data2)
                    vv= verif_vehi_exist(vehi)
                    if (vv == "vehicule autorise"):
                        client_socket.sendall('Votre vehicule est autorise\n'.encode('utf-8'))
                        print("En attente due l'id parking...")
                        client_socket.sendall('En attente de l id parking...\n'.encode('utf-8'))
                        data3 = client_socket.recv(1024).decode('utf-8').rstrip('\n').strip()
                        idparking = (data3)
                        vp=verif_parkingexist(idparking)
                        if(vp == "PARKING OUI"):
                            result2 = maj_cap_max(idparking)
                            if (result2 > 0):
                                result = creer_reserv_véhicule(idparking, vehi)
                                if(result == "RESERVATION PRISE EN COMPTE"):
                                    client_socket.sendall('Votre reservation a bien ete prise en compte\n'.encode('utf-8'))
                                else :
                                    client_socket.sendall('erreur lors de la reservation\n'.encode('utf-8'))
                            else : 
                                client_socket.sendall('Il n y a plus de place dans ce parking\n'.encode('utf-8'))
                        else :
                            client_socket.sendall('ce parking n existe pas\n'.encode('utf-8'))

                    else : 
                        client_socket.sendall('Votre vehicule n est pas autorise sur nos parking\n'.encode('utf-8'))

                else :
                    test = verif_est_un_membre(carte)
                    if (test == "carte inexistante"):
                        client_socket.sendall('ID carte invalide\n'.encode('utf-8'))
                        
                    else : 
                        client_socket.sendall('Desole votre abonnement ne permet pas d avoir acces au parking\n'.encode('utf-8'))



             


        except socket.timeout:
            print("Délai de réponse depasse. La connexion avec le client sera fermee.")
            client_socket.sendall('Delai de reponse depasse. La connexion sera fermee.\n'.encode('utf-8'))


        except Exception as ex:
            print(f'ERREUR')
            