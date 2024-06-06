"""
    Fichier : gestion_credentials_wtf_forms.py
    Auteur : OM 2021.03.22
    Gestion des formulaires avec WTF
"""
from flask_wtf import FlaskForm
from wtforms import StringField, DateField
from wtforms import SubmitField
from wtforms.fields.numeric import IntegerField
from wtforms.fields.simple import HiddenField
from wtforms.validators import Length, InputRequired, DataRequired, NumberRange
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
    password_credentials_update_wtf = StringField("Password", validators=[Length(min=2, max=20, message="min 2 max 40")])
    submit = SubmitField("Update")


class FormWTFDeletecredentials(FlaskForm):
    nom_credentials_delete_wtf = StringField("Email", validators=[DataRequired()])
    submit_btn_annuler = SubmitField("Annuler")
    submit_btn_conf_del = SubmitField("Confirmer la suppression")
    submit_btn_del = SubmitField("Supprimer définitivement")

class FormWTFAjouterLiaison(FlaskForm):
    FK_Personne= IntegerField("ID Personne", validators=[DataRequired(), NumberRange(min=1, message="Veuillez entrer un ID valide.")])
    FK_Credentials = IntegerField("ID Credentials", validators=[DataRequired(), NumberRange(min=1, message="Veuillez entrer un ID valide.")])
    submit = SubmitField("Ajouter Liaison")

class FormWTFUpdateLiaison(FlaskForm):
    ID_Personne_Credentials = IntegerField("ID Liaison", validators=[DataRequired()])
    FK_Personne_wtf = IntegerField("ID Personne", validators=[DataRequired(), NumberRange(min=1, message="Veuillez entrer un ID valide.")])
    FK_Credentials_wtf = IntegerField("ID Credentials", validators=[DataRequired(), NumberRange(min=1, message="Veuillez entrer un ID valide.")])
    submit = SubmitField("Mettre à jour Liaison")

