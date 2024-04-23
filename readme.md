# OneTrain

## Description
OneTrain est une application conçue pour les jeunes joueurs de football ainsi que pour leurs entraîneurs. Elle offre la possibilité de consulter le calendrier des prochains matchs et permet aux entraîneurs de gérer les événements ainsi que le matériel nécessaire pour les entraînements et les matchs.

## Fonctionnalités
- **Calendrier des matchs :** Les jeunes joueurs peuvent consulter facilement les dates, heures et lieux des prochains matchs de leur équipe.
- **Gestion des événements :** Les entraîneurs peuvent ajouter, modifier ou supprimer des événements tels que des entraînements, des matchs, des réunions, etc.
- **Gestion du matériel :** Les entraîneurs ont la possibilité de vérifier le matériel disponible et de passer des commandes pour les équipements nécessaires.

## Comment utiliser
1. **Inscription/Connexion :** Les utilisateurs doivent s'inscrire pour accéder à l'application en tant que joueur ou entraîneur.
2. **Calendrier :** Une fois connectés, les joueurs peuvent consulter leur calendrier pour connaître les dates et les détails des prochains matchs.
3. **Gestion des événements :** Les entraîneurs ont accès à des fonctionnalités supplémentaires pour gérer les événements tels que l'ajout, la modification ou la suppression.
4. **Gestion du matériel :** Les entraîneurs peuvent vérifier le matériel disponible et passer des commandes si nécessaire.

## Technologies utilisées
- Frontend : HTML, CSS, JavaScript
- Backend : Python, Flask
- Base de données : MariaDB avec phpMyAdmin
## Installation

1. Clonez le repository : 
    ```bash
    git clone git@github.com:OneTrain-app/OneTrain.git OneTrain
    ```
2. Accedez au projet :
    ```bash
    cd OneTrain
    ```
   
3. Désactivez git :
   - Sur Linux/macOS : 
        ```bash
        rm -rf .git
        ```
    - Sur Windows : 
        ```powershell
        rmdir /s .git
        ```

4. Créez un environnement virtuel : 
    ```bash
    python3 -m venv .venv
    ```
   
5. Activez l'environnement virtuel :
    - Sur Linux/macOS : 
        ```bash
        source .venv/bin/activate
        ```
    - Sur Windows : 
        ```powershell
        .venv\Scripts\activate
        ```

6. Mettez à jour pip : 
    ```bash
    python -m pip install --upgrade pip
    ```

7. Installez les dépendances : 
    ```bash
    pip install -r requirements.txt
    ```

8. Pour lancer docker : 
    ```bash
    docker-compose up
    ```

## Contributeurs
- José Gomes


## Remarques
- Ce projet est en cours de développement. Toute contribution est la bienvenue !
- Pour toute question ou problème, veuillez ouvrir une issue sur GitHub.
