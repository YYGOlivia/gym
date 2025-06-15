-- Insérer un nouveau membre, Yige YANG
INSERT INTO Personne (id_personne, nom, prénom, sexe, num_téléphone, adress_mail, login, mot_de_passe, id_carte)
VALUES ('A4', 'YANG', 'Yige', 'F', '0123456789', 'yygolivia@gmail.com', 'Yige1234', 'Yige@1#2', NULL);

-- Créer une nouvelle carte pour Yige YANG
INSERT INTO Carte (id_carte, type_carte, date_achat, date_expiration)
VALUES ('carteA004', 'Membre', '2023-11-13', '2024-11-13');

-- Associer le nouveau membre Yige YANG à sa carte
UPDATE Personne SET id_carte = 'carteA004' WHERE id_personne = 'A4';

-- Ajouter Yige YANG en tant que membre de type 'Classique'
INSERT INTO Membre (id_membre, type_membre)
VALUES ('A4', 'Classique');

-- Réserver un cours de Yoga pour Yige YANG
INSERT INTO Abonnement (id_abonnement, date_début, date_fin, id_membre, id_cours)
VALUES ('abonnement006', '2023-11-13', '2023-12-31', 'A4', 'cours001');

-- Ajouter les informations sur le véhicule de Yige YANG
INSERT INTO Véhicule (id_véhicule, type_véhicule, id_parking)
VALUES ('véhicule', 'voiture', 'parking001');

-- Enregistrer une entrée dans le portique pour Yige YANG
INSERT INTO Scanne (id_portique, id_carte) VALUES ('portiqueA2', 'carteA004');
