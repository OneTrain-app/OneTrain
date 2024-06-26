"""Gestion des "routes" FLASK et des données pour les genres.
Fichier : gestion_genres_crud.py
Auteur : OM 2021.03.16
"""
from pathlib import Path

from flask import redirect
from flask import request
from flask import session
from flask import url_for

from APP_FILMS_164 import app
from APP_FILMS_164.database.database_tools import DBconnection
from APP_FILMS_164.erreurs.exceptions import *
from APP_FILMS_164.genres.gestion_genres_wtf_forms import FormWTFAjouterGenres
from APP_FILMS_164.genres.gestion_genres_wtf_forms import FormWTFDeleteGenre
from APP_FILMS_164.genres.gestion_genres_wtf_forms import FormWTFUpdateGenre

"""
    Auteur : OM 2021.03.16
    Définition d'une "route" /genres_afficher
    
    Test : ex : http://127.0.0.1:5575/genres_afficher
    
    Paramètres : order_by : ASC : Ascendant, DESC : Descendant
                id_genre_sel = 0 >> tous les genres.
                id_genre_sel = "n" affiche le genre dont l'id est "n"
"""




@app.route("/genres_afficher/<string:order_by>/<int:id_genre_sel>", methods=['GET', 'POST'])
def genres_afficher(order_by, id_genre_sel):
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                strsql_genres_afficher = """
                SELECT ID_Personne, Prenom, Nom
                FROM T_Personne
                """
                mc_afficher.execute(strsql_genres_afficher)

                data_genres = mc_afficher.fetchall()

                if not data_genres:
                    flash("""La table est vide mon gars. !!""", "warning")
                else:
                    flash(f"Voici les gens mon ami <3 !!", "success")

        except Exception as Exception_genres_afficher:
            raise ExceptionGenresAfficher(f"Archive: {Path(__file__).name}; "
                                          f"{genres_afficher.__name__}; "
                                          f"{Exception_genres_afficher}")

    return render_template("genres/genres_afficher.html", data=data_genres)



"""
    Auteur : OM 2021.03.22
    Définition d'une "route" /genres_ajouter
    
    Test : ex : http://127.0.0.1:5575/genres_ajouter
    
    Paramètres : sans
    
    But : Ajouter un genre pour un film
    
    Remarque :  Dans le champ "name_genre_html" du formulaire "genres/genres_ajouter.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""


@app.route("/genres_ajouter", methods=['GET', 'POST'])
def genres_ajouter_wtf():
    form = FormWTFAjouterGenres()
    if request.method == "POST":
        try:
            if form.validate_on_submit():
                prenom = form.Prenom_wtf.data
                nom = form.Nom_wtf.data

                # Insérer les données dans la table T_Personne
                strsql_insert_personne = """INSERT INTO T_Personne (Prenom, Nom) 
                            VALUES (%(prenom)s, %(nom)s)"""

                valeurs_insertion_personne = {
                    "prenom": prenom,
                    "nom": nom
                }
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_insert_personne, valeurs_insertion_personne)

                flash(f"Données insérées !!", "success")

                # Rediriger vers la page d'affichage des genres
                return redirect(url_for('genres_afficher', order_by='DESC', id_genre_sel=0))

        except Exception as e:
            flash(f"Une erreur s'est produite : {str(e)}", "error")

    return render_template("genres/genres_ajouter_wtf.html", form=form)




"""
    Auteur : OM 2021.03.29
    Définition d'une "route" /genre_update
    
    Test : ex cliquer sur le menu "genres" puis cliquer sur le bouton "EDIT" d'un "genre"
    
    Paramètres : sans
    
    But : Editer(update) un genre qui a été sélectionné dans le formulaire "genres_afficher.html"
    
    Remarque :  Dans le champ "nom_genre_update_wtf" du formulaire "genres/genre_update_wtf.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""


@app.route("/genre_update", methods=['GET', 'POST'])
def genre_update_wtf():
    # L'utilisateur vient de cliquer sur le bouton "EDIT". Récupère la valeur de "id_genre"
    id_genre_update = request.values['id_genre_btn_edit_html']

    # Création d'un objet formulaire pour l'UPDATE
    form_update = FormWTFUpdateGenre()
    try:
        # 2023.05.14 OM S'il y a des listes déroulantes dans le formulaire, 
        # la validation pose parfois des problèmes.
        if request.method == "POST" and form_update.submit.data:
            # Récupérer la valeur du champ "nom_genre_update_wtf" depuis le formulaire "genre_update_wtf.html"
            # après avoir cliqué sur "SUBMIT". Puis convertir cette valeur en lettres minuscules.
            name_genre_update = form_update.nom_genre_update_wtf.data
            name_genre_update = name_genre_update.lower()

            # Récupérer la valeur du champ "date_genre_wtf_essai" depuis le formulaire.
            date_genre_essai = form_update.date_genre_wtf_essai.data

            # Créer un dictionnaire pour les valeurs à mettre à jour
            valeur_update_dictionnaire = {
                "value_id_genre": id_genre_update,
                "value_name_genre": name_genre_update,
                "value_date_genre_essai": date_genre_essai
            }
            print("valeur_update_dictionnaire ", valeur_update_dictionnaire)

            # Requête SQL pour mettre à jour les informations du genre dans la base de données
            str_sql_update_intitulegenre = """UPDATE T_Personne SET Nom = %(value_name_genre)s, 
                                              Prenom = %(value_date_genre_essai)s 
                                              WHERE ID_Personne = %(value_id_genre)s """
            # Exécution de la requête avec gestion automatique de la connexion à la base de données
            with DBconnection() as mconn_bd:
                mconn_bd.execute(str_sql_update_intitulegenre, valeur_update_dictionnaire)

            # Affichage d'un message flash pour informer l'utilisateur que la mise à jour a été effectuée avec succès
            flash(f"Donnée mise à jour !!", "success")
            print(f"Donnée mise à jour !!")

            # Redirection vers la page d'affichage des genres avec l'ID du genre mis à jour
            return redirect(url_for('genres_afficher', order_by="ASC", id_genre_sel=id_genre_update))

        elif request.method == "GET":
            # Requête SQL pour récupérer les informations du genre à partir de l'ID fourni
            str_sql_id_genre = """SELECT ID_Personne, Nom, Prenom FROM T_Personne 
                                  WHERE ID_Personne = %(value_id_genre)s"""
            valeur_select_dictionnaire = {"value_id_genre": id_genre_update}

            # Exécution de la requête avec gestion automatique de la connexion à la base de données
            with DBconnection() as mybd_conn:
                mybd_conn.execute(str_sql_id_genre, valeur_select_dictionnaire)

                # Récupération d'une seule ligne de résultat
                data_nom_genre = mybd_conn.fetchone()

            # Vérifier que des données ont été retournées
            if data_nom_genre:
                print("Prenom ", data_nom_genre, " type ", type(data_nom_genre), " genre ",
                      data_nom_genre["Nom"])

                # Afficher la valeur sélectionnée dans les champs du formulaire "genre_update_wtf.html"
                form_update.nom_genre_update_wtf.data = data_nom_genre["Prenom"]
                form_update.date_genre_wtf_essai.data = data_nom_genre["Nom"]
            else:
                # Si aucune donnée n'est trouvée, afficher un message d'erreur et rediriger
                flash(f"Erreur : Aucun enregistrement trouvé pour l'ID {id_genre_update}", "danger")
                return redirect(url_for('genres_afficher', order_by="ASC"))

    except Exception as Exception_genre_update_wtf:
        # Gestion des exceptions et levée d'une exception personnalisée
        raise ExceptionGenreUpdateWtf(f"fichier : {Path(__file__).name}  ;  "
                                      f"{genre_update_wtf.__name__} ; "
                                      f"{Exception_genre_update_wtf}")

    # Rendu du template avec le formulaire de mise à jour
    return render_template("genres/genre_update_wtf.html", form_update=form_update)


"""
    Auteur : OM 2021.04.08
    Définition d'une "route" /genre_delete
    
    Test : ex. cliquer sur le menu "genres" puis cliquer sur le bouton "DELETE" d'un "genre"
    
    Paramètres : sans
    
    But : Effacer(delete) un genre qui a été sélectionné dans le formulaire "genres_afficher.html"
    
    Remarque :  Dans le champ "nom_genre_delete_wtf" du formulaire "genres/genre_delete_wtf.html",
                le contrôle de la saisie est désactivée. On doit simplement cliquer sur "DELETE"
"""



@app.route("/genre_delete", methods=['GET', 'POST'])
def genre_delete_wtf():
    data_films_attribue_genre_delete = None
    btn_submit_del = None
    id_genre_delete = request.values.get('id_genre_btn_delete_html')

    form_delete = FormWTFDeleteGenre()
    try:
        if request.method == "POST" and form_delete.validate_on_submit():
            if form_delete.submit_btn_annuler.data:
                return redirect(url_for("genres_afficher", order_by="ASC", id_genre_sel=0))

            if form_delete.submit_btn_conf_del.data:
                data_films_attribue_genre_delete = session.get('data_films_attribue_genre_delete')
                flash(f"Effacer le genre de façon définitive de la BD !!!", "danger")
                btn_submit_del = True

            if form_delete.submit_btn_del.data:
                valeur_delete_dictionnaire = {"value_id_genre": id_genre_delete}

                str_sql_delete_films_genre = """DELETE FROM T_Personne_Credentials WHERE FK_Personne = %(value_id_genre)s"""
                str_sql_delete_idgenre = """DELETE FROM T_Personne WHERE ID_Personne = %(value_id_genre)s"""
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(str_sql_delete_films_genre, valeur_delete_dictionnaire)
                    mconn_bd.execute(str_sql_delete_idgenre, valeur_delete_dictionnaire)

                flash(f"Genre définitivement effacé !!", "success")
                return redirect(url_for('genres_afficher', order_by="ASC", id_genre_sel=0))

        if request.method == "GET":
            valeur_select_dictionnaire = {"value_id_genre": id_genre_delete}

            str_sql_genres_films_delete = """
            SELECT ID_Personne_Credentials, Email, T_Credentials.ID_Credentials, Nom 
            FROM T_Personne_Credentials 
            INNER JOIN T_Credentials ON T_Personne_Credentials.FK_Credentials = T_Credentials.ID_Credentials 
            INNER JOIN T_Personne ON T_Personne_Credentials.FK_Personne = T_Personne.ID_Personne 
            WHERE FK_Personne = %(value_id_genre)s
            """

            with DBconnection() as mydb_conn:
                mydb_conn.execute(str_sql_genres_films_delete, valeur_select_dictionnaire)
                data_films_attribue_genre_delete = mydb_conn.fetchall()

                session['data_films_attribue_genre_delete'] = data_films_attribue_genre_delete

                str_sql_id_genre = "SELECT ID_Personne, Prenom FROM T_Personne WHERE ID_Personne = %(value_id_genre)s"
                mydb_conn.execute(str_sql_id_genre, valeur_select_dictionnaire)
                data_nom_genre = mydb_conn.fetchone()

            form_delete.nom_genre_delete_wtf.data = data_nom_genre["Prenom"]
            btn_submit_del = False

    except Exception as e:
        print(f"Une erreur est survenue: {e}")
        flash(f"Erreur: {e}", "danger")

    return render_template("genres/genre_delete_wtf.html",
                           form_delete=form_delete,
                           btn_submit_del=btn_submit_del,
                           data_films_associes=data_films_attribue_genre_delete)

if __name__ == "__main__":
    app.run(debug=True)
