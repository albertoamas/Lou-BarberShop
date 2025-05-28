from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TelField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from app.models.usuario import Usuario

class LoginForm(FlaskForm):
    """Formulario para inicio de sesión"""
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    remember_me = BooleanField('Recordarme')
    submit = SubmitField('Iniciar Sesión')

class RegistroForm(FlaskForm):
    """Formulario para registro de usuarios"""
    nombre = StringField('Nombre Completo', validators=[DataRequired(), Length(min=3, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    telefono = TelField('Teléfono', validators=[DataRequired(), Length(min=8, max=20)])
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField(
        'Confirmar Contraseña', 
        validators=[DataRequired(), EqualTo('password', message='Las contraseñas deben coincidir')]
    )
    submit = SubmitField('Registrarse')
    
    def validate_email(self, email):
        """Valida que el email no esté ya registrado"""
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('Este email ya está registrado. Por favor utilice otro o inicie sesión.')
