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
from APP_FILMS_164.films.gestion_films_wtf_forms import FormWTFUpdateFilm
from APP_FILMS_164.credentials.gestion_credentials_wtf_forms import FormWTFDeletecredentials

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
    form_update = FormWTFUpdateFilm()
    try:
        # 2023.05.14 OM S'il y a des listes déroulantes dans le formulaire, 
        # la validation pose parfois des problèmes.
        if request.method == "POST" and form_update.submit.data:
            # Récupérer la valeur du champ "nom_credentials_update_wtf" depuis le formulaire "credentials_update_wtf.html"
            # après avoir cliqué sur "SUBMIT". Puis convertir cette valeur en lettres minuscules.
            name_credentials_update = form_update.nom_credentials_update_wtf.data
            name_credentials_update = name_credentials_update.lower()

            # Récupérer la valeur du champ "date_credentials_wtf_essai" depuis le formulaire.
            date_credentials_essai = form_update.date_credentials_wtf_essai.data

            # Créer un dictionnaire pour les valeurs à mettre à jour
            valeur_update_dictionnaire = {
                "value_id_credentials": id_credentials_update,
                "value_name_credentials": name_credentials_update,
                "value_date_credentials_essai": date_credentials_essai
            }
            print("valeur_update_dictionnaire ", valeur_update_dictionnaire)

            # Requête SQL pour mettre à jour les informations du credentials dans la base de données
            str_sql_update_intitulecredentials = """UPDATE T_Personne SET Nom = %(value_name_credentials)s, 
                                              Prenom = %(value_date_credentials_essai)s 
                                              WHERE ID_Personne = %(value_id_credentials)s """
            # Exécution de la requête avec gestion automatique de la connexion à la base de données
            with DBconnection() as mconn_bd:
                mconn_bd.execute(str_sql_update_intitulecredentials, valeur_update_dictionnaire)

            # Affichage d'un message flash pour informer l'utilisateur que la mise à jour a été effectuée avec succès
            flash(f"Donnée mise à jour !!", "success")
            print(f"Donnée mise à jour !!")

            # Redirection vers la page d'affichage des credentials avec l'ID du credentials mis à jour
            return redirect(url_for('credentials_afficher', order_by="ASC", id_credentials_sel=id_credentials_update))

        elif request.method == "GET":
            # Requête SQL pour récupérer les informations du credentials à partir de l'ID fourni
            str_sql_id_credentials = """SELECT ID_Personne, Nom, Prenom FROM T_Personne 
                                  WHERE ID_Personne = %(value_id_credentials)s"""
            valeur_select_dictionnaire = {"value_id_credentials": id_credentials_update}

            # Exécution de la requête avec gestion automatique de la connexion à la base de données
            with DBconnection() as mybd_conn:
                mybd_conn.execute(str_sql_id_credentials, valeur_select_dictionnaire)

                # Récupération d'une seule ligne de résultat
                data_nom_credentials = mybd_conn.fetchone()

            # Vérifier que des données ont été retournées
            if data_nom_credentials:
                print("Prenom ", data_nom_credentials, " type ", type(data_nom_credentials), " credentials ",
                      data_nom_credentials["Nom"])

                # Afficher la valeur sélectionnée dans les champs du formulaire "credentials_update_wtf.html"
                form_update.nom_credentials_update_wtf.data = data_nom_credentials["Prenom"]
                form_update.date_credentials_wtf_essai.data = data_nom_credentials["Nom"]
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
    return render_template("films/films_update_wtf.html", form_update=form_update)


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
    data_films_attribue_credentials_delete = None
    btn_submit_del = None
    id_credentials_delete = request.values.get('id_credentials_btn_delete_html')

    form_delete = FormWTFDeletecredentials()
    try:
        if request.method == "POST" and form_delete.validate_on_submit():
            if form_delete.submit_btn_annuler.data:
                return redirect(url_for("credentials_afficher", order_by="ASC", id_credentials_sel=0))

            if form_delete.submit_btn_conf_del.data:
                data_films_attribue_credentials_delete = session.get('data_films_attribue_credentials_delete')
                flash(f"Effacer le credentials de façon définitive de la BD !!!", "danger")
                btn_submit_del = True

            if form_delete.submit_btn_del.data:
                valeur_delete_dictionnaire = {"value_id_credentials": id_credentials_delete}

                str_sql_delete_films_credentials = """DELETE FROM T_Personne_Credentials WHERE FK_Personne = %(value_id_credentials)s"""
                str_sql_delete_idcredentials = """DELETE FROM T_Personne WHERE ID_Personne = %(value_id_credentials)s"""
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(str_sql_delete_films_credentials, valeur_delete_dictionnaire)
                    mconn_bd.execute(str_sql_delete_idcredentials, valeur_delete_dictionnaire)

                flash(f"credentials définitivement effacé !!", "success")
                return redirect(url_for('credentials_afficher', order_by="ASC", id_credentials_sel=0))

        if request.method == "GET":
            valeur_select_dictionnaire = {"value_id_credentials": id_credentials_delete}

            str_sql_credentials_films_delete = """
            SELECT ID_Personne_Credentials, Email, T_Credentials.ID_Credentials, Nom 
            FROM T_Personne_Credentials 
            INNER JOIN T_Credentials ON T_Personne_Credentials.FK_Credentials = T_Credentials.ID_Credentials 
            INNER JOIN T_Personne ON T_Personne_Credentials.FK_Personne = T_Personne.ID_Personne 
            WHERE FK_Personne = %(value_id_credentials)s
            """

            with DBconnection() as mydb_conn:
                mydb_conn.execute(str_sql_credentials_films_delete, valeur_select_dictionnaire)
                data_films_attribue_credentials_delete = mydb_conn.fetchall()

                session['data_films_attribue_credentials_delete'] = data_films_attribue_credentials_delete

                str_sql_id_credentials = "SELECT ID_Personne, Prenom FROM T_Personne WHERE ID_Personne = %(value_id_credentials)s"
                mydb_conn.execute(str_sql_id_credentials, valeur_select_dictionnaire)
                data_nom_credentials = mydb_conn.fetchone()

            form_delete.nom_credentials_delete_wtf.data = data_nom_credentials["Prenom"]
            btn_submit_del = False

    except Exception as e:
        print(f"Une erreur est survenue: {e}")
        flash(f"Erreur: {e}", "danger")

    return render_template("films/films_delete_wtf.html",
                           form_delete=form_delete,
                           btn_submit_del=btn_submit_del,
                           data_films_associes=data_films_attribue_credentials_delete)

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


