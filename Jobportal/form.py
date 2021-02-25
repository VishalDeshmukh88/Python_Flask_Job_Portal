from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed
from wtforms import StringField, PasswordField,SelectField,TextAreaField,TextField, SubmitField, BooleanField,IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo,ValidationError
from Jobportal.models import User
from flask_login import current_user
import phonenumbers


class RegistrationForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',validators=[DataRequired(), Email()])
    contact=StringField('Contact',validators=[DataRequired()])
    address = TextAreaField('Address',validators=[Length(max=200)])
    skills = TextAreaField('Skills',validators=[Length(max=200)])
    gender = SelectField('Gender', choices=[("Male"),("Female")])
    education=TextField('Education',validators=[Length(max=50)])
    certifications=TextAreaField("Certifications",validators=[Length(max=50)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

    def validate_phone(self, contact):
        try:
            p = phonenumbers.parse(contact.data)
            if not phonenumbers.is_valid_number(p):
                raise ValueError()
        except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
            raise ValidationError('Invalid phone number')

class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(), Length(min=2, max=20)])
    contact = IntegerField('Contact', validators=[DataRequired()])
    address = TextAreaField('Address', validators=[Length(max=200)])
    skills = TextAreaField('Skills', validators=[Length(max=200)])
    gender = SelectField('Gender', choices=[("Male"), ("Female")])
    education = TextField('Education', validators=[Length(max=50)])
    certifications = TextAreaField("Certifications", validators=[Length(max=50)])
    picture=FileField("Update Profile Picture",validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data!= current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data!=current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')

    def validate_phone(self, contact):
        try:
            p = phonenumbers.parse(contact.data)
            if not phonenumbers.is_valid_number(p):
                raise ValueError()
        except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
            raise ValidationError('Invalid phone number')