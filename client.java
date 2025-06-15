import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;

public class client {
    public static void main(String[] args) {
        PrintWriter writer = null;
        BufferedReader reader = null;
        BufferedReader responseReader = null;
        String serverHost = "localhost"; // Adresse IP ou nom d'hôte du serveur Python
        int serverPort = 65433; // Port utilisé par le serveur Python
        Socket socket = null;

        

        try {

            
            socket = new Socket(serverHost, serverPort);
            socket.setSoTimeout(5000);
            writer = new PrintWriter(socket.getOutputStream(), true);
            reader = new BufferedReader(new InputStreamReader(System.in));
            responseReader = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            String r = responseReader.readLine();
            System.out.println(r);
            String choixUtilisateur = reader.readLine();
            writer.println(choixUtilisateur);
        

            if (choixUtilisateur.equals("1")) {

                // Envoi de la demande au serveur
                String r2 = responseReader.readLine();
                System.out.println(r2);
                String idC = reader.readLine();
                String data = idC;
                writer.println(data);
                System.out.println("Données envoyées au serveur.");
                String response = responseReader.readLine();
                System.out.println("Réponse du serveur : " + response);
                if (response.equals("Votre carte et votre abonnement sont valides")) {
                    String r3 = responseReader.readLine();
                    System.out.println(r3);
                    String idP = reader.readLine();
                    String data2 = idP;
                    writer.println(data2);
                    System.out.println("Données envoyées au serveur.");
                    String response2 = responseReader.readLine();
                    System.out.println("Réponse du serveur : " + response2);}
                    
                
            }
            

            else if (choixUtilisateur.equals("2")){

                String r2 = responseReader.readLine();
                System.out.println(r2);
                String carte = reader.readLine();
                String data = carte;
                writer.println(data);
                System.out.println("Données envoyées au serveur.");
                String response = responseReader.readLine();
                System.out.println("Réponse du serveur : " + response);
                if (response.equals("Vous possedez un abonnement premium, poursuite de la reservation")) {
                    String r3 = responseReader.readLine();
                    System.out.println(r3);
                    String vehi = reader.readLine();
                    String data2 = vehi;
                    writer.println(data2);
                    System.out.println("Données envoyées au serveur.");
                    String response2 = responseReader.readLine();
                    System.out.println("Réponse du serveur : " + response2);
                        if (response2.equals("Votre vehicule est autorise")) {
                        String r4 = responseReader.readLine();
                        System.out.println(r4);
                        String idparking = reader.readLine();
                        String data3 = idparking;
                        writer.println(data3);
                        System.out.println("Données envoyées au serveur.");
                        String response3 = responseReader.readLine();
                        System.out.println("Réponse du serveur : " + response3);
                        }
                }
                else if (response.equals("Vous etes un employe, poursuite de la reservation")) {
                    String r5 = responseReader.readLine();
                    System.out.println(r5);
                    String vehi = reader.readLine();
                    String data2 = vehi;
                    writer.println(data2);
                    System.out.println("Données envoyées au serveur.");
                    String response2 = responseReader.readLine();
                    System.out.println("Réponse du serveur : " + response2);
                        if (response2.equals("Votre vehicule est autorise")) {
                        String r6 = responseReader.readLine();
                        System.out.println(r6);
                        String idparking = reader.readLine();
                        String data3 = idparking;
                        writer.println(data3);
                        System.out.println("Données envoyées au serveur.");
                        String response3 = responseReader.readLine();
                        System.out.println("Réponse du serveur : " + response3);
                        }
                }
            }
                
                    

                /*System.out.println("Pour quelle salle souhaitez-vous effectuer une réservation de place de parking ? (entrez ID du parking)");
                String idparking = reader.readLine();

                System.out.println("Quel type de véhicule utilisez-vous ?");
                String vehi = reader.readLine();

                 // Concaténer les deux informations avec un délimiteur (par exemple, une virgule)
                String data = idparking + "," + vehi;
            
                writer.println(data);
                System.out.println("Données envoyées au serveur.");

                // Lecture de la réponse du serveur
                String response = responseReader.readLine();
                System.out.println("Réponse du serveur : " + response);*/

            
                

        } catch (IOException e) {
            e.printStackTrace();
        }
        // Attendre l'entrée de l'utilisateur après la fermeture des ressources
        try {
            System.out.println("Appuyez sur Entrée pour continuer...");
            reader = new BufferedReader(new InputStreamReader(System.in));
            reader.readLine();
            reader.close();
            writer.close();
            socket.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}