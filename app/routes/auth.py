from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from urllib.parse import urlparse
from app import db
from app.forms import LoginForm, RegistroForm
from app.models.usuario import Usuario
from app.models.role import Role

# Crear blueprint para autenticación
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Ruta para iniciar sesión"""
    # Si el usuario ya está autenticado, redirigir a la página principal
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        # Buscar al usuario por su email
        user = Usuario.query.filter_by(email=form.email.data).first()
        
        # Verificar si el usuario existe y la contraseña es correcta
        if user is None or not user.check_password(form.password.data):
            flash('Email o contraseña incorrectos', 'danger')
            return redirect(url_for('auth.login'))        # Iniciar sesión y redirigir
        login_user(user, remember=form.remember_me.data)
        
        # Redirigir a la página que el usuario intentaba visitar
        next_page = request.args.get('next')
        if not next_page or next_page.startswith('http') or next_page.startswith('//'):
            next_page = url_for('main.index')
        
        flash('¡Has iniciado sesión correctamente!', 'success')
        return redirect(next_page)
    
    return render_template('auth/login.html', title='Iniciar Sesión', form=form)

@auth_bp.route('/logout')
def logout():
    """Ruta para cerrar sesión"""
    logout_user()
    flash('Has cerrado sesión correctamente', 'info')
    return redirect(url_for('main.index'))

@auth_bp.route('/registro', methods=['GET', 'POST'])
def registro():
    """Ruta para registrar un nuevo usuario"""
    # Si el usuario ya está autenticado, redirigir a la página principal
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = RegistroForm()
    if form.validate_on_submit():
        # Obtener el rol de cliente
        role = Role.query.filter_by(nombre='cliente').first()
        if not role:
            flash('Error en el sistema de roles', 'danger')
            return redirect(url_for('auth.registro'))
        
        # Crear nuevo usuario
        user = Usuario(
            nombre=form.nombre.data,
            email=form.email.data,
            telefono=form.telefono.data,
            rol_id=role.id
        )
        user.password = form.password.data
        
        # Guardar en la base de datos
        db.session.add(user)
        db.session.commit()
        
        flash('¡Te has registrado correctamente! Ahora puedes iniciar sesión', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/registro.html', title='Registro', form=form)

@auth_bp.route('/perfil')
@login_required
def perfil():
    """Ruta para ver el perfil del usuario"""
    return render_template('auth/perfil.html', title='Mi Perfil')
