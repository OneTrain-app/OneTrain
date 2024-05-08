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
                if order_by == "ASC" and id_genre_sel == 0:
                    strsql_genres_afficher = """
                    SELECT T_Personne.id_Personne, T_Personne.Nom, T_Personne.Prenom, T_Credentials.Password, T_Credentials.Email 
                    FROM T_Personne 
                    INNER JOIN T_Credentials ON T_Personne.ID_Credentials = T_Credentials.ID_Credentials
                    """
                    mc_afficher.execute(strsql_genres_afficher)
                elif order_by == "ASC":
                    valeur_id_genre_selected_dictionnaire = {"value_id_Personne_selected": id_genre_sel}
                    strsql_genres_afficher = """
                    SELECT T_Personne.id_Personne, T_Personne.Nom, T_Personne.Prenom, T_Credentials.Password, T_Credentials.Email 
                    FROM T_Personne 
                    INNER JOIN T_Credentials ON T_Personne.ID_Credentials = T_Credentials.ID_Credentials
                    WHERE T_Personne.id_Personne = %(value_id_Personne_selected)s
                    """
                    mc_afficher.execute(strsql_genres_afficher, valeur_id_genre_selected_dictionnaire)
                else:
                    strsql_genres_afficher = """
                    SELECT T_Personne.id_Personne, T_Personne.Nom, T_Personne.Prenom, T_Credentials.Password, T_Credentials.Email 
                    FROM T_Personne 
                    INNER JOIN T_Credentials ON T_Personne.ID_Credentials = T_Credentials.ID_Credentials
                    ORDER BY T_Personne.id_Personne DESC
                    """
                    mc_afficher.execute(strsql_genres_afficher)

                data_genres = mc_afficher.fetchall()

                if not data_genres and id_genre_sel == 0:
                    flash("""La table est vide mon gars. !!""", "warning")
                elif not data_genres and id_genre_sel > 0:
                    flash(f"Tu cherches qui wsh???!!", "warning")
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
                id_role = form.id_role_wtf.data
                mail = form.Mail_wtf.data
                password = form.Password_wtf.data
                nom = form.Nom_wtf.data

                # Insérer les données dans la table T_Credentials
                strsql_insert_credentials = """INSERT INTO T_Credentials (Email, Password) 
                            VALUES (%(mail)s, %(password)s)"""

                valeurs_insertion_credentials = {
                    "mail": mail,
                    "password": password,
                }
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_insert_credentials, valeurs_insertion_credentials)
                    id_credentials_inseree = mconn_bd.lastrowid

                # Insérer les données dans la table T_Personne
                strsql_insert_personne = """INSERT INTO T_Personne (Prenom, ID_Role, Nom, ID_Credentials) 
                            VALUES (%(prenom)s, %(id_role)s, %(nom)s, %(id_credentials)s)"""

                valeurs_insertion_personne = {
                    "prenom": prenom,
                    "id_role": id_role,
                    "nom": nom,
                    "id_credentials": id_credentials_inseree
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

    # Objet formulaire pour l'UPDATE
    form_update = FormWTFUpdateGenre()
    try:
        # 2023.05.14 OM S'il y a des listes déroulantes dans le formulaire
        # La validation pose quelques problèmes
        if request.method == "POST" and form_update.submit.data:
            # Récupèrer la valeur du champ depuis "genre_update_wtf.html" après avoir cliqué sur "SUBMIT".
            # Puis la convertir en lettres minuscules.
            name_genre_update = form_update.nom_genre_update_wtf.data
            name_genre_update = name_genre_update.lower()
            date_genre_essai = form_update.date_genre_wtf_essai.data

            valeur_update_dictionnaire = {"value_id_genre": id_genre_update,
                                          "value_name_genre": name_genre_update,
                                          "value_date_genre_essai": date_genre_essai
                                          }
            print("valeur_update_dictionnaire ", valeur_update_dictionnaire)

            str_sql_update_intitulegenre = """UPDATE t_genre SET intitule_genre = %(value_name_genre)s, 
            date_ins_genre = %(value_date_genre_essai)s WHERE id_genre = %(value_id_genre)s """
            with DBconnection() as mconn_bd:
                mconn_bd.execute(str_sql_update_intitulegenre, valeur_update_dictionnaire)

            flash(f"Donnée mise à jour !!", "success")
            print(f"Donnée mise à jour !!")

            # afficher et constater que la donnée est mise à jour.
            # Affiche seulement la valeur modifiée, "ASC" et l'"id_genre_update"
            return redirect(url_for('genres_afficher', order_by="ASC", id_genre_sel=id_genre_update))
        elif request.method == "GET":
            # Opération sur la BD pour récupérer "id_genre" et "intitule_genre" de la "t_genre"
            str_sql_id_genre = "SELECT id_genre, intitule_genre, date_ins_genre FROM t_genre " \
                               "WHERE id_genre = %(value_id_genre)s"
            valeur_select_dictionnaire = {"value_id_genre": id_genre_update}
            with DBconnection() as mybd_conn:
                mybd_conn.execute(str_sql_id_genre, valeur_select_dictionnaire)
            # Une seule valeur est suffisante "fetchone()", vu qu'il n'y a qu'un seul champ "nom genre" pour l'UPDATE
            data_nom_genre = mybd_conn.fetchone()
            print("data_nom_genre ", data_nom_genre, " type ", type(data_nom_genre), " genre ",
                  data_nom_genre["intitule_genre"])

            # Afficher la valeur sélectionnée dans les champs du formulaire "genre_update_wtf.html"
            form_update.nom_genre_update_wtf.data = data_nom_genre["intitule_genre"]
            form_update.date_genre_wtf_essai.data = data_nom_genre["date_ins_genre"]

    except Exception as Exception_genre_update_wtf:
        raise ExceptionGenreUpdateWtf(f"fichier : {Path(__file__).name}  ;  "
                                      f"{genre_update_wtf.__name__} ; "
                                      f"{Exception_genre_update_wtf}")

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
    data_credentials_associated_person_delete = None
    btn_submit_del = None
    
    # L'utilisateur vient de cliquer sur le bouton "DELETE". Récupère la valeur de "id_personne"
    id_personne_delete = request.values['id_genre_btn_delete_html']

    # Objet formulaire pour effacer la personne sélectionnée.
    form_delete = FormWTFDeleteGenre()
    try:
        if request.method == "POST" and form_delete.validate_on_submit():

            if form_delete.submit_btn_annuler.data:
                return redirect(url_for("genres_afficher", order_by="ASC", id_genre_sel=0))

            if form_delete.submit_btn_conf_del.data:
                # Récupérer les données pour afficher à nouveau
                # le formulaire "genres/genre_delete_wtf.html" lorsque le bouton "Etes-vous sûr de vouloir effacer ?" est cliqué.
                data_credentials_associated_person_delete = session['data_credentials_associated_person_delete']
                flash(f"Effacer la personne définitivement de la base de données !!!", "danger")
                btn_submit_del = True

            if form_delete.submit_btn_del.data:
                valeur_delete_dictionnaire = {"value_Id_Personne": id_personne_delete}

                # Requêtes SQL pour supprimer toutes les informations liées au nom de la personne dans toutes les tables associées
                str_sql_delete_personne_credentials = """DELETE FROM T_Personne_Credentials WHERE fk_personne = %(value_Id_Personne)s"""
                str_sql_delete_personne = """DELETE FROM T_Personne WHERE id_personne = %(value_Id_Personne)s"""
                # Ajoutez d'autres requêtes de suppression pour chaque table associée à la personne ici
                
                # Exécution des requêtes SQL
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(str_sql_delete_personne_credentials, valeur_delete_dictionnaire)
                    mconn_bd.execute(str_sql_delete_personne, valeur_delete_dictionnaire)
                    # Exécutez les autres requêtes de suppression ici
                
                flash(f"Toutes les informations liées à la personne ont été définitivement effacées !!", "success")

                # Afficher les données
                return redirect(url_for('genres_afficher', order_by="ASC", id_genre_sel=0))

        if request.method == "GET":
            valeur_select_dictionnaire = {"value_id_personne": id_personne_delete}

            # Requête pour obtenir toutes les informations associées à la personne que l'utilisateur veut effacer
            str_sql_personne_credentials_delete = """SELECT T_Personne.id_personne, T_Personne.nom, T_Personne.prenom, T_Credentials.id_credentials 
                                         FROM T_Personne 
                                         INNER JOIN T_Personne_Credentials 
                                         ON T_Personne.id_personne = T_Personne_Credentials.fk_personne
                                         INNER JOIN T_Credentials 
                                         ON T_Personne_Credentials.fk_credentials = T_Credentials.id_credentials
                                         WHERE T_Personne.id_personne = %(value_id_personne)s"""


            with DBconnection() as mydb_conn:
                mydb_conn.execute(str_sql_personne_credentials_delete, valeur_select_dictionnaire)
                data_credentials_associated_person_delete = mydb_conn.fetchall()

                # Mémoriser les données pour afficher à nouveau
                # le formulaire "genres/genre_delete_wtf.html" lorsque le bouton "Etes-vous sûr de vouloir effacer ?" est cliqué.
                session['data_credentials_associated_person_delete'] = data_credentials_associated_person_delete

                # Opération sur la BD pour récupérer les informations de la personne
                str_sql_personne_info = "SELECT id_personne, nom, prenom FROM T_Personne WHERE id_personne = %(value_id_personne)s"
                mydb_conn.execute(str_sql_personne_info, valeur_select_dictionnaire)
                data_personne_info = mydb_conn.fetchone()

            # Vérifier si les informations de la personne existent
            if data_personne_info is not None:
                # Afficher les informations de la personne sélectionnée dans le formulaire "genre_delete_wtf.html"
                form_delete.nom_personne_delete_wtf.data = data_personne_info["nom"]
                form_delete.prenom_personne_delete_wtf.data = data_personne_info["prenom"]

            btn_submit_del = False

    except Exception as Exception_genre_delete_wtf:
        raise ExceptionGenreDeleteWtf(f"fichier : {Path(__file__).name}  ;  "
                                      f"{genre_delete_wtf.__name__} ; "
                                      f"{Exception_genre_delete_wtf}")

    return render_template("genres/genre_delete_wtf.html",
                           form_delete=form_delete,
                           btn_submit_del=btn_submit_del,
                           data_credentials_associated_person_delete=data_credentials_associated_person_delete)
