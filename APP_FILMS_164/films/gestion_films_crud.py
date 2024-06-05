"""Gestion des "routes" FLASK et des données pour les films.
Fichier : gestion_films_crud.py
Auteur : OM 2022.04.11
"""
from pathlib import Path

from flask import redirect
from flask import request
from flask import session
from flask import url_for
from flask import render_template, flash

from APP_films_164.database.database_tools import DBconnection
from APP_films_164.erreurs.exceptions import *
from APP_films_164.films.gestion_films_wtf_forms import FormWTFUpdatefilms, FormWTFAddfilms, FormWTFDeletefilms

@app.route("/films_afficher", methods=['GET', 'POST'])
def films_afficher():
    try:
        with DBconnection() as mc_afficher:
            strsql_afficher = """SELECT * FROM T_films"""
            mc_afficher.execute(strsql_afficher)
            data = mc_afficher.fetchall()
            print("data ", data)

            if not data:
                flash("""La table "T_films" est vide. Rien à afficher""", "warning")
            else:
                flash(f"Données de la table 'T_films' affichées", "success")

            return render_template("films/films_afficher.html", data=data)

    except Exception as Exception_films_afficher:
        raise ExceptionfilmsAfficher(f"fichier : {Path(__file__).name}  ;  "
                                           f"{films_afficher.__name__} ; "
                                           f"{Exception_films_afficher}")

# ... (le reste du code)

@app.route("/films_add", methods=['GET', 'POST'])
def films_add_wtf():
    # Objet formulaire pour AJOUTER un credential
    form_add_films = FormWTFAddfilms()
    if request.method == "POST":
        try:
            if form_add_films.validate_on_submit():
                email_add = form_add_films.nom_films_add_wtf.data
                password_add = form_add_films.prenom_films_add_wtf.data

                valeurs_insertion_dictionnaire = {"value_email": email_add, "value_password": password_add}
                print("valeurs_insertion_dictionnaire ", valeurs_insertion_dictionnaire)

                strsql_insert_credential = """INSERT INTO T_films (Email, Password) 
                                                               VALUES (%(value_email)s, %(value_password)s) """
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_insert_credential, valeurs_insertion_dictionnaire)

                flash(f"Données insérées !!", "success")
                print(f"Données insérées !!")

                # Pour afficher et constater l'insertion du nouveau credential
                return redirect(url_for('films_genres_afficher', id_films_sel=0, order_by='ASC'))

        except Exception as Exception_genres_ajouter_wtf:
            raise ExceptionGenresAjouterWtf(f"fichier : {Path(__file__).name}  ;  "
                                            f"{films_add_wtf.__name__} ; "
                                            f"{Exception_genres_ajouter_wtf}")

    return render_template("films/films_add_wtf.html", form_add_films=form_add_films)

"""Editer(update) un films qui a été sélectionné dans le formulaire "films_genres_afficher.html"
Auteur : OM 2022.04.11
Définition d'une "route" /films_update

Test : exemple: cliquer sur le menu "films/Genres" puis cliquer sur le bouton "EDIT" d'un "films"

Paramètres : sans

But : Editer(update) un genre qui a été sélectionné dans le formulaire "genres_afficher.html"

Remarque :  Dans le champ "nom_films_update_wtf" du formulaire "films/films_update_wtf.html",
            le contrôle de la saisie s'effectue ici en Python.
            On ne doit pas accepter un champ vide.
"""


@app.route("/films_update", methods=['GET', 'POST'])
def films_update_wtf():
    # L'utilisateur vient de cliquer sur le bouton "EDIT". Récupère la valeur de "id_films"
    id_films_update = request.values['id_films_btn_edit_html']

    # Objet formulaire pour l'UPDATE
    form_update_films = FormWTFUpdatefilms()
    try:
        # 2023.05.14 OM S'il y a des listes déroulantes dans le formulaire
        # La validation pose quelques problèmes
        if request.method == "POST" and form_update_films.submit.data:
            # Récupèrer la valeur du champ depuis "genre_update_wtf.html" après avoir cliqué sur "SUBMIT".
            nom_films_update = form_update_films.nom_films_update_wtf.data
            duree_films_update = form_update_films.duree_films_update_wtf.data
            description_films_update = form_update_films.description_films_update_wtf.data
            cover_link_films_update = form_update_films.cover_link_films_update_wtf.data
            datesortie_films_update = form_update_films.datesortie_films_update_wtf.data

            valeur_update_dictionnaire = {"value_id_films": id_films_update,
                                          "value_nom_films": nom_films_update,
                                          "value_duree_films": duree_films_update,
                                          "value_description_films": description_films_update,
                                          "value_cover_link_films": cover_link_films_update,
                                          "value_datesortie_films": datesortie_films_update
                                          }
            print("valeur_update_dictionnaire ", valeur_update_dictionnaire)

            str_sql_update_nom_films = """UPDATE t_films SET nom_films = %(value_nom_films)s,
                                                            duree_films = %(value_duree_films)s,
                                                            description_films = %(value_description_films)s,
                                                            cover_link_films = %(value_cover_link_films)s,
                                                            date_sortie_films = %(value_datesortie_films)s
                                                            WHERE id_films = %(value_id_films)s"""
            with DBconnection() as mconn_bd:
                mconn_bd.execute(str_sql_update_nom_films, valeur_update_dictionnaire)

            flash(f"Donnée mise à jour !!", "success")
            print(f"Donnée mise à jour !!")

            # afficher et constater que la donnée est mise à jour.
            # Afficher seulement le films modifié, "ASC" et l'"id_films_update"
            return redirect(url_for('films_genres_afficher', id_films_sel=id_films_update))
        elif request.method == "GET":
            # Opération sur la BD pour récupérer "id_films" et "intitule_genre" de la "t_genre"
            str_sql_id_films = "SELECT * FROM t_films WHERE id_films = %(value_id_films)s"
            valeur_select_dictionnaire = {"value_id_films": id_films_update}
            with DBconnection() as mybd_conn:
                mybd_conn.execute(str_sql_id_films, valeur_select_dictionnaire)
            # Une seule valeur est suffisante "fetchone()", vu qu'il n'y a qu'un seul champ "nom genre" pour l'UPDATE
            data_films = mybd_conn.fetchone()
            print("data_films ", data_films, " type ", type(data_films), " genre ",
                  data_films["nom_films"])

            # Afficher la valeur sélectionnée dans le champ du formulaire "films_update_wtf.html"
            form_update_films.nom_films_update_wtf.data = data_films["nom_films"]
            form_update_films.duree_films_update_wtf.data = data_films["duree_films"]
            # Debug simple pour contrôler la valeur dans la console "run" de PyCharm
            print(f" duree films  ", data_films["duree_films"], "  type ", type(data_films["duree_films"]))
            form_update_films.description_films_update_wtf.data = data_films["description_films"]
            form_update_films.cover_link_films_update_wtf.data = data_films["cover_link_films"]
            form_update_films.datesortie_films_update_wtf.data = data_films["date_sortie_films"]

    except Exception as Exception_films_update_wtf:
        raise ExceptionfilmsUpdateWtf(f"fichier : {Path(__file__).name}  ;  "
                                     f"{films_update_wtf.__name__} ; "
                                     f"{Exception_films_update_wtf}")

    return render_template("films/films_update_wtf.html", form_update_films=form_update_films)


"""Effacer(delete) un films qui a été sélectionné dans le formulaire "films_genres_afficher.html"
Auteur : OM 2022.04.11
Définition d'une "route" /films_delete
    
Test : ex. cliquer sur le menu "films" puis cliquer sur le bouton "DELETE" d'un "films"
    
Paramètres : sans

Remarque :  Dans le champ "nom_films_delete_wtf" du formulaire "films/films_delete_wtf.html"
            On doit simplement cliquer sur "DELETE"
"""


@app.route("/films_delete", methods=['GET', 'POST'])
def films_delete_wtf():
    # Pour afficher ou cacher les boutons "EFFACER"
    data_films_delete = None
    btn_submit_del = None
    # L'utilisateur vient de cliquer sur le bouton "DELETE". Récupère la valeur de "id_films"
    id_films_delete = request.values['id_films_btn_delete_html']

    # Objet formulaire pour effacer le films sélectionné.
    form_delete_films = FormWTFDeletefilms()
    try:
        # Si on clique sur "ANNULER", afficher tous les films.
        if form_delete_films.submit_btn_annuler.data:
            return redirect(url_for("films_genres_afficher", id_films_sel=0))

        if form_delete_films.submit_btn_conf_del_films.data:
            # Récupère les données afin d'afficher à nouveau
            # le formulaire "films/films_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
            data_films_delete = session['data_films_delete']
            print("data_films_delete ", data_films_delete)

            flash(f"Effacer le films de façon définitive de la BD !!!", "danger")
            # L'utilisateur vient de cliquer sur le bouton de confirmation pour effacer...
            # On affiche le bouton "Effacer genre" qui va irrémédiablement EFFACER le genre
            btn_submit_del = True

        # L'utilisateur a vraiment décidé d'effacer.
        if form_delete_films.submit_btn_del_films.data:
            valeur_delete_dictionnaire = {"value_id_films": id_films_delete}
            print("valeur_delete_dictionnaire ", valeur_delete_dictionnaire)

            str_sql_delete_fk_films_genre = """DELETE FROM t_genre_films WHERE fk_films = %(value_id_films)s"""
            str_sql_delete_films = """DELETE FROM t_films WHERE id_films = %(value_id_films)s"""
            # Manière brutale d'effacer d'abord la "fk_films", même si elle n'existe pas dans la "t_genre_films"
            # Ensuite on peut effacer le films vu qu'il n'est plus "lié" (INNODB) dans la "t_genre_films"
            with DBconnection() as mconn_bd:
                mconn_bd.execute(str_sql_delete_fk_films_genre, valeur_delete_dictionnaire)
                mconn_bd.execute(str_sql_delete_films, valeur_delete_dictionnaire)

            flash(f"films définitivement effacé !!", "success")
            print(f"films définitivement effacé !!")

            # afficher les données
            return redirect(url_for('films_genres_afficher', id_films_sel=0))
        if request.method == "GET":
            valeur_select_dictionnaire = {"value_id_films": id_films_delete}
            print(id_films_delete, type(id_films_delete))

            # Requête qui affiche le films qui doit être efffacé.
            str_sql_genres_films_delete = """SELECT * FROM t_films WHERE id_films = %(value_id_films)s"""

            with DBconnection() as mydb_conn:
                mydb_conn.execute(str_sql_genres_films_delete, valeur_select_dictionnaire)
                data_films_delete = mydb_conn.fetchall()
                print("data_films_delete...", data_films_delete)

                # Nécessaire pour mémoriser les données afin d'afficher à nouveau
                # le formulaire "films/films_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                session['data_films_delete'] = data_films_delete

            # Le bouton pour l'action "DELETE" dans le form. "films_delete_wtf.html" est caché.
            btn_submit_del = False

    except Exception as Exception_films_delete_wtf:
        raise ExceptionfilmsDeleteWtf(f"fichier : {Path(__file__).name}  ;  "
                                     f"{films_delete_wtf.__name__} ; "
                                     f"{Exception_films_delete_wtf}")

    return render_template("films/films_delete_wtf.html",
                           form_delete_films=form_delete_films,
                           btn_submit_del=btn_submit_del,
                           data_films_del=data_films_delete
                           )
