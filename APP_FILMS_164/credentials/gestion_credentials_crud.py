"""Gestion des "routes" FLASK et des données pour les credentials.
Fichier : gestion_credentials_crud.py
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
from APP_FILMS_164.credentials.gestion_credentials_wtf_forms import FormWTFAjoutercredentials
from APP_FILMS_164.credentials.gestion_credentials_wtf_forms import FormWTFDeletecredentials
from APP_FILMS_164.credentials.gestion_credentials_wtf_forms import FormWTFUpdatecredentials
from APP_FILMS_164.credentials.gestion_credentials_wtf_forms import FormWTFDeletecredentials
from APP_FILMS_164.credentials.gestion_credentials_wtf_forms import FormWTFAjouterLiaison
from APP_FILMS_164.credentials.gestion_credentials_wtf_forms import FormWTFUpdateLiaison

"""
    Auteur : OM 2021.03.16
    Définition d'une "route" /credentials_afficher
    
    Test : ex : http://127.0.0.1:5575/credentials_afficher
    from APP_FILMS_164.films import gestion_films_crud
    from APP_FILMS_164.films import gestion_films_wtf_forms
    Paramètres : order_by : ASC : Ascendant, DESC : Descendant
                id_credentials_sel = 0 >> tous les credentials.
                id_credentials_sel = "n" affiche le credentials dont l'id est "n"
"""




@app.route("/credentials_afficher/<string:order_by>/<int:id_credentials_sel>", methods=['GET', 'POST'])
def credentials_afficher(order_by, id_credentials_sel):
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                strsql_credentials_afficher = """
                SELECT *
                FROM T_Credentials
                """
                mc_afficher.execute(strsql_credentials_afficher)

                data_credentials = mc_afficher.fetchall()

                if not data_credentials:
                    flash("""La table est vide mon gars. !!""", "warning")
                else:
                    flash(f"Voici les gens mon ami <3 !!", "success")

        except Exception as Exception_credentials_afficher:
            raise ExceptioncredentialsAfficher(f"Archive: {Path(__file__).name}; "
                                          f"{credentials_afficher.__name__}; "
                                          f"{Exception_credentials_afficher}")

    return render_template("credentials/credentials_afficher.html", data=data_credentials)



"""
    Auteur : OM 2021.03.22
    Définition d'une "route" /credentials_ajouter
    
    Test : ex : http://127.0.0.1:5575/credentials_ajouter
    
    Paramètres : sans
    
    But : Ajouter un credentials pour un film
    
    Remarque :  Dans le champ "name_credentials_html" du formulaire "credentials/credentials_ajouter.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""


@app.route("/credentials_ajouter", methods=['GET', 'POST'])
def credentials_ajouter_wtf():
    form = FormWTFAjoutercredentials()
    if request.method == "POST":
        try:
            if form.validate_on_submit():
                email = form.Email_wtf.data
                password = form.Password_wtf.data

                # Insérer les données dans la table T_Personne
                strsql_insert_personne = """INSERT INTO T_Credentials (Email, Password) 
                            VALUES (%(email)s, %(password)s)"""

                valeurs_insertion_personne = {
                    "email": email,
                    "password": password
                }
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_insert_personne, valeurs_insertion_personne)

                flash(f"Données insérées !!", "success")

                # Rediriger vers la page d'affichage des credentials
                return redirect(url_for('credentials_afficher', order_by='DESC', id_credentials_sel=0))

        except Exception as e:
            flash(f"Une erreur s'est produite : {str(e)}", "error")

    return render_template("credentials/credentials_ajouter_wtf.html", form=form)




"""
    Auteur : OM 2021.03.29
    Définition d'une "route" /credentials_update
    
    Test : ex cliquer sur le menu "credentials" puis cliquer sur le bouton "EDIT" d'un "credentials"
    
    Paramètres : sans
    
    But : Editer(update) un credentials qui a été sélectionné dans le formulaire "credentials_afficher.html"
    
    Remarque :  Dans le champ "nom_credentials_update_wtf" du formulaire "credentials/credentials_update_wtf.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""


@app.route("/credentials_update", methods=['GET', 'POST'])
def credentials_update_wtf():
    # L'utilisateur vient de cliquer sur le bouton "EDIT". Récupère la valeur de "id_credentials"
    id_credentials_update = request.values['id_credentials_btn_edit_html']

    # Création d'un objet formulaire pour l'UPDATE
    form_update = FormWTFUpdatecredentials()
    try:
        # 2023.05.14 OM S'il y a des listes déroulantes dans le formulaire, 
        # la validation pose parfois des problèmes.
        if request.method == "POST" and form_update.submit.data:
            # Récupérer la valeur du champ "email_credentials_update_wtf" depuis le formulaire "credentials_update_wtf.html"
            email_credentials_update = form_update.email_credentials_update_wtf.data

            # Récupérer la valeur du champ "password_credentials_update_wtf" depuis le formulaire.
            password_credentials_update = form_update.password_credentials_update_wtf.data

            # Créer un dictionnaire pour les valeurs à mettre à jour
            valeur_update_dictionnaire = {
                "value_id_credentials": id_credentials_update,
                "value_email_credentials": email_credentials_update,
                "value_password_credentials": password_credentials_update
            }
            print("valeur_update_dictionnaire ", valeur_update_dictionnaire)

            # Requête SQL pour mettre à jour les informations du credentials dans la base de données
            str_sql_update_credentials = """UPDATE T_Credentials 
                                             SET Email = %(value_email_credentials)s, 
                                                 Password = %(value_password_credentials)s 
                                             WHERE ID_Credentials = %(value_id_credentials)s """
            # Exécution de la requête avec gestion automatique de la connexion à la base de données
            with DBconnection() as mconn_bd:
                mconn_bd.execute(str_sql_update_credentials, valeur_update_dictionnaire)

            # Affichage d'un message flash pour informer l'utilisateur que la mise à jour a été effectuée avec succès
            flash(f"Donnée mise à jour !!", "success")
            print(f"Donnée mise à jour !!")

            # Redirection vers la page d'affichage des credentials avec l'ID du credentials mis à jour
            return redirect(url_for('credentials_afficher', order_by="ASC", id_credentials_sel=id_credentials_update))

        elif request.method == "GET":
            # Requête SQL pour récupérer les informations du credentials à partir de l'ID fourni
            str_sql_id_credentials = """SELECT ID_Credentials, Email, Password FROM T_Credentials 
                                        WHERE ID_Credentials = %(value_id_credentials)s"""
            valeur_select_dictionnaire = {"value_id_credentials": id_credentials_update}

            # Exécution de la requête avec gestion automatique de la connexion à la base de données
            with DBconnection() as mybd_conn:
                mybd_conn.execute(str_sql_id_credentials, valeur_select_dictionnaire)

                # Récupération d'une seule ligne de résultat
                data_credentials = mybd_conn.fetchone()

            # Vérifier que des données ont été retournées
            if data_credentials:
                print("Email ", data_credentials, " type ", type(data_credentials), " credentials ",
                      data_credentials["Email"])

                # Afficher la valeur sélectionnée dans les champs du formulaire "credentials_update_wtf.html"
                form_update.email_credentials_update_wtf.data = data_credentials["Email"]
                form_update.password_credentials_update_wtf.data = data_credentials["Password"]
            else:
                # Si aucune donnée n'est trouvée, afficher un message d'erreur et rediriger
                flash(f"Erreur : Aucun enregistrement trouvé pour l'ID {id_credentials_update}", "danger")
                return redirect(url_for('credentials_afficher', order_by="ASC"))

    except Exception as Exception_credentials_update_wtf:
        # Gestion des exceptions et levée d'une exception personnalisée
        raise ExceptioncredentialsUpdateWtf(f"fichier : {Path(__file__).name}  ;  "
                                            f"{credentials_update_wtf.__name__} ; "
                                            f"{Exception_credentials_update_wtf}")

    # Rendu du template avec le formulaire de mise à jour
    return render_template("credentials/credentials_update_wtf.html", form_update=form_update)

"""
    Auteur : OM 2021.04.08
    Définition d'une "route" /credentials_delete
    
    Test : ex. cliquer sur le menu "credentials" puis cliquer sur le bouton "DELETE" d'un "credentials"
    
    Paramètres : sans
    
    But : Effacer(delete) un credentials qui a été sélectionné dans le formulaire "credentials_afficher.html"
    
    Remarque :  Dans le champ "nom_credentials_delete_wtf" du formulaire "credentials/credentials_delete_wtf.html",
                le contrôle de la saisie est désactivée. On doit simplement cliquer sur "DELETE"
"""


@app.route("/credentials_delete", methods=['GET', 'POST'])
def credentials_delete_wtf():
    data_credentials_delete = None
    btn_submit_del = None
    id_credentials_delete = request.values.get('id_credentials_btn_delete_html')

    form_delete = FormWTFDeletecredentials()
    try:
        if request.method == "POST" and form_delete.validate_on_submit():
            if form_delete.submit_btn_annuler.data:
                return redirect(url_for("credentials_afficher", order_by="ASC", id_credentials_sel=0))

            if form_delete.submit_btn_conf_del.data:
                data_credentials_delete = session.get('data_credentials_delete')
                flash(f"Effacer les credentials de façon définitive de la BD !!!", "danger")
                btn_submit_del = True

            if form_delete.submit_btn_del.data:
                valeur_delete_dictionnaire = {"value_id_credentials": id_credentials_delete}

                # Supprimer d'abord les entrées dans T_Personne_Role qui référencent T_Personne
                str_sql_delete_personne_role = """DELETE FROM T_Personne_Role WHERE FK_Personne = %(value_id_credentials)s"""
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(str_sql_delete_personne_role, valeur_delete_dictionnaire)

                # Supprimer ensuite les entrées dans T_Personne_Credentials qui référencent T_Credentials
                str_sql_delete_personne_credentials = """DELETE FROM T_Personne_Credentials WHERE FK_Credentials = %(value_id_credentials)s"""
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(str_sql_delete_personne_credentials, valeur_delete_dictionnaire)

                # Supprimer ensuite les entrées dans T_Personne qui référencent T_Credentials
                str_sql_delete_personne = """DELETE FROM T_Personne WHERE ID_Credentials = %(value_id_credentials)s"""
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(str_sql_delete_personne, valeur_delete_dictionnaire)

                # Ensuite, supprimer les entrées dans T_Credentials
                str_sql_delete_idcredentials = """DELETE FROM T_Credentials WHERE ID_Credentials = %(value_id_credentials)s"""
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(str_sql_delete_idcredentials, valeur_delete_dictionnaire)

                flash(f"Credentials définitivement effacés !!", "success")
                return redirect(url_for('credentials_afficher', order_by="ASC", id_credentials_sel=0))

        if request.method == "GET":
            valeur_select_dictionnaire = {"value_id_credentials": id_credentials_delete}

            str_sql_credentials_delete = """SELECT ID_Credentials, Email, Password FROM T_Credentials 
                                             WHERE ID_Credentials = %(value_id_credentials)s"""
            with DBconnection() as mydb_conn:
                mydb_conn.execute(str_sql_credentials_delete, valeur_select_dictionnaire)
                data_credentials_delete = mydb_conn.fetchone()

                session['data_credentials_delete'] = data_credentials_delete

            form_delete.nom_credentials_delete_wtf.data = data_credentials_delete["Email"]
            btn_submit_del = False

    except Exception as e:
        print(f"Une erreur est survenue: {e}")
        flash(f"Erreur: {e}", "danger")

    return render_template("credentials/credentials_delete_wtf.html",
                           form_delete=form_delete,
                           btn_submit_del=btn_submit_del,
                           data_credentials=data_credentials_delete)

if __name__ == "__main__":
    app.run(debug=True)




@app.route("/personne_credentials_afficher/<string:order_by>/<int:id_personne_credentials_sel>", methods=['GET', 'POST'])
def personne_credentials_afficher(order_by, id_personne_credentials_sel):
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                strsql_personne_credentials_afficher = """
               SELECT 
                                                            ph.ID_Personne_Credentials, 
                                                            p.ID_Personne, 
                                                            p.Nom, 
                                                            p.Prenom, 
                                                        
                                                            h.ID_Credentials, 
                                                            h.Email,
                                                            h.Password 
                                                        FROM 
                                                            T_Personne p
                                                        JOIN 
                                                            T_Personne_Credentials ph ON p.ID_Personne = ph.FK_Personne
                                                        JOIN 
                                                            T_Credentials h ON ph.FK_Credentials = h.ID_Credentials
                                                        ORDER BY 
                                                            ph.ID_Personne_Credentials ASC;
                """
                mc_afficher.execute(strsql_personne_credentials_afficher)

                data_personne_credentials = mc_afficher.fetchall()

                if not data_personne_credentials:
                    flash("""La table est vide mon gars. !!""", "warning")
                else:
                    flash(f"Voici les gens mon ami <3 !!", "success")

        except Exception as Exception_personne_credentials_afficher:
            raise Exceptionpersonne_credentialsAfficher(f"Archive: {Path(__file__).name}; "
                                          f"{personne_credentials_afficher.__name__}; "
                                          f"{Exception_personne_credentials_afficher}")

    return render_template("credentials/personne_credentials_afficher.html", data=data_personne_credentials)

@app.route("/liaison_ajouter", methods=['GET', 'POST'])
def liaison_ajouter_wtf():
    form = FormWTFAjouterLiaison()
    if request.method == "POST":
        try:
            if form.validate_on_submit():
                FK_Personne = form.FK_Personne.data
                FK_Credentials = form.FK_Credentials.data

                valeurs_insertion_dictionnaire = {"FK_Personne": FK_Personne, "FK_Credentials": FK_Credentials}

                strsql_insert_liaison = """INSERT INTO T_Personne_Credentials (FK_Personne, FK_Credentials) VALUES (%(FK_Personne)s, %(FK_Credentials)s);"""
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_insert_liaison, valeurs_insertion_dictionnaire)

                flash("Liaison ajoutée !!", "success")
                return redirect(url_for('credentials_afficher', order_by='DESC', id_credentials_sel=0))

        except Exception as Exception_liaison_ajouter_wtf:
            raise ExceptionGenresAjouterWtf(f"fichier : {Path(__file__).name}  ;  "
                                            f"{liaison_ajouter_wtf.__name__} ; "
                                            f"{Exception_liaison_ajouter_wtf}")

    return render_template("credentials/personne_credentials_ajouter_wtf.html", form=form)

@app.route("/liaison_update", methods=['GET', 'POST'])
def liaison_update_wtf():
    form_update = FormWTFUpdateLiaison()

    if request.method == "GET":
        ID_Personne_Credentials_update = request.args.get('ID_Personne_Credentials')
        if ID_Personne_Credentials_update:
            # Charger les données existantes pour remplir le formulaire
            str_sql_liaison = """SELECT ID_Personne_Credentials, FK_Personne, FK_Credentials 
                                 FROM T_Personne_Credentials
                                 WHERE ID_Personne_Credentials = %(value_ID_Personne_Credentials)s"""
            valeur_select_dictionnaire = {"value_ID_Personne_Credentials": ID_Personne_Credentials_update}
            try:
                with DBconnection() as mybd_conn:
                    mybd_conn.execute(str_sql_liaison, valeur_select_dictionnaire)
                    data_liaison = mybd_conn.fetchone()

                    if data_liaison:
                        form_update.ID_Personne_Credentials.data = data_liaison["ID_Personne_Credentials"]
                        form_update.FK_Personne_wtf.data = data_liaison["FK_Personne"]
                        form_update.FK_Credentials_wtf.data = data_liaison["FK_Credentials"]
                    else:
                        flash(f"La liaison avec l'ID {ID_Personne_Credentials_update} n'existe pas.", "danger")
                        return redirect(url_for('personne_credentials_afficher', order_by="ASC", id_personne_credentials_sel=0))
            except Exception as Exception_liaison_update_wtf:
                raise ExceptionGenreUpdateWtf(
                    f"fichier : {Path(__file__).name}  ;  "
                    f"{liaison_update_wtf.__name__} ; "
                    f"{Exception_liaison_update_wtf}"
                )

    elif request.method == "POST":
        ID_Personne_Credentials_update = form_update.ID_Personne_Credentials.data  # Récupérer l'ID depuis le champ caché
        if not ID_Personne_Credentials_update:
            flash("Aucun ID de liaison n'a été fourni pour la mise à jour.", "danger")
            return redirect(url_for('personne_credentials_afficher', order_by="ASC", id_personne_credentials_sel=0))

        if form_update.validate_on_submit():
            FK_Personne = form_update.FK_Personne_wtf.data
            FK_Credentials = form_update.FK_Credentials_wtf.data

            valeur_update_dictionnaire = {
                "ID_Personne_Credentials": ID_Personne_Credentials_update,
                "FK_Personne": FK_Personne,
                "FK_Credentials": FK_Credentials
            }

            str_sql_update_liaison = """UPDATE T_Personne_Credentials
                                        SET FK_Personne = %(FK_Personne)s, FK_Credentials = %(FK_Credentials)s 
                                        WHERE ID_Personne_Credentials = %(ID_Personne_Credentials)s"""
            try:
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(str_sql_update_liaison, valeur_update_dictionnaire)
                flash("Liaison mise à jour !!", "success")
                return redirect(url_for('personne_credentials_afficher', order_by="ASC", id_personne_credentials_sel=ID_Personne_Credentials_update))
            except Exception as Exception_liaison_update_wtf:
                raise ExceptionGenreUpdateWtf(
                    f"fichier : {Path(__file__).name}  ;  "
                    f"{liaison_update_wtf.__name__} ; "
                    f"{Exception_liaison_update_wtf}"
                )

    return render_template("credentials/personne_credentials_update_wtf.html", form_update=form_update, ID_Personne_Credentials=ID_Personne_Credentials_update)
@app.route("/materiel_afficher/<string:order_by>/<int:id_materiel_sel>", methods=['GET', 'POST'])
def materiel_afficher(order_by, id_materiel_sel):
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                strsql_materiel_afficher = """
                SELECT ID_Materiel, Nom, Quantite, Description
                FROM T_Materiel
                """
                mc_afficher.execute(strsql_materiel_afficher)

                data_materiel = mc_afficher.fetchall()

                if not data_materiel:
                    flash("La table est vide.", "warning")
                else:
                    flash("Voici le matériel disponible.", "success")

        except Exception as Exception_materiel_afficher:
            raise ExceptionMaterielAfficher(f"Archive: {Path(__file__).name}; "
                                            f"{materiel_afficher.__name__}; "
                                            f"{Exception_materiel_afficher}")

    return render_template("materiel/materiel_afficher.html", data=data_materiel)

