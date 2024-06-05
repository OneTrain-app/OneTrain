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
    Nom_wtf = StringField("Nom", validators=[Length(min=2, max=20, message="min 2 max 20")])
    Prenom_wtf = StringField("Prenom", validators=[Length(min=2, max=20, message="min 2 max 20")])


    submit = SubmitField("Enregistrer personne")


class FormWTFUpdatecredentials(FlaskForm):
    """
        Formulaire pour mettre à jour le nom et le prénom d'une personne.
    """
    nom_credentials_update_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    nom_credentials_update_wtf = StringField("Clavioter le nom ", validators=[
        Length(min=2, max=20, message="min 2 max 20"),
        Regexp(nom_credentials_update_regexp, message="Pas de chiffres, de caractères spéciaux, d'espace à double, de double apostrophe, de double trait d'union")
    ])
    
    date_credentials_wtf_essai_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    date_credentials_wtf_essai = StringField("Clavioter le prénom ", validators=[
        Length(min=2, max=20, message="min 2 max 20"),
        Regexp(date_credentials_wtf_essai_regexp, message="Pas de chiffres, de caractères spéciaux, d'espace à double, de double apostrophe, de double trait d'union")
    ])
    
    submit = SubmitField("Update Personne")


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