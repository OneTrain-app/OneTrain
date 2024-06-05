"""
    Fichier : gestion_credentials_wtf_forms.py
    Auteur : OM 2021.03.22
    Gestion des formulaires avec WTF
"""
from flask_wtf import FlaskForm
from wtforms import StringField, DateField
from wtforms import SubmitField
from wtforms.validators import Length, InputRequired, DataRequired
from wtforms.validators import Regexp


class FormWTFAjoutercredentials(FlaskForm):
    """
        Dans le formulaire "credentials_ajouter_wtf.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    Email_wtf = StringField("Email", validators=[Length(min=2, max=20, message="min 2 max 40")])
    Password_wtf = StringField("Password", validators=[Length(min=2, max=20, message="min 2 max 20")])


    submit = SubmitField("Enregistrer personne")

class FormWTFUpdatecredentials(FlaskForm):
    email_credentials_update_wtf = StringField("Email", validators=[Length(min=2, max=20, message="min 2 max 40")])
    password_credentials_update_wtf = StringField("Password", validators=[Length(min=2, max=20, message="min 2 max 20")])
    submit = SubmitField("Update")


class FormWTFDeletecredentials(FlaskForm):
    """
        Dans le formulaire "credentials_delete_wtf.html"

        nom_credentials_delete_wtf : Champ qui reçoit la valeur du credentials, lecture seule. (readonly=true)
        submit_btn_del : Bouton d'effacement "DEFINITIF".
        submit_btn_conf_del : Bouton de confirmation pour effacer un "credentials".
        submit_btn_annuler : Bouton qui permet d'afficher la table "t_credentials".
    """
    nom_credentials_delete_wtf = StringField("Effacer ce credentials", render_kw={'readonly': True})
    submit_btn_del = SubmitField("Effacer Définitivement")
    submit_btn_conf_del = SubmitField("Confirmer l'Effacement")
    submit_btn_annuler = SubmitField("Annuler")