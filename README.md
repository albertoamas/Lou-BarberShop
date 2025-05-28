# Lou Barbershop - Sistema de Reservas

Aplicación web para gestionar reservas de citas en una barbería. Proyecto final para el curso de Tecnología Web II.

## Características

- **Sistema de Autenticación**: Registro e inicio de sesión de usuarios
- **Gestión de Perfiles**: Usuarios pueden ver y editar su información personal
- **Reserva de Citas**: Sistema completo para agendar, modificar y cancelar citas
- **Panel de Administración**: Para gestionar reservas, servicios, empleados y horarios
- **API Interna**: Para la obtención dinámica de horarios disponibles

## Tecnologías Utilizadas

- **Backend**: Flask con SQLAlchemy y PostgreSQL
- **Frontend**: HTML, CSS, JavaScript con Bootstrap 5
- **Autenticación**: Flask-Login para gestión de sesiones
- **Formularios**: Flask-WTF para validación de datos
- **Migraciones**: Flask-Migrate para control de cambios en la base de datos

## Requisitos

- Python 3.10 o superior
- PostgreSQL
- Miniconda o Anaconda (recomendado)

## Instalación

1. Clonar el repositorio:

```bash
git clone <URL_DEL_REPOSITORIO>
cd TrabajoFinal
```

2. Crear y activar un entorno virtual con Miniconda:

```bash
conda create --prefix ./env python=3.10
conda activate ./env
```

3. Instalar las dependencias:

```bash
pip install -r requirements.txt
```

4. Configurar las variables de entorno en un archivo `.env`:

```
FLASK_APP=app
FLASK_DEBUG=1
SECRET_KEY=clave_secreta_aqui
DATABASE_URL=postgresql://usuario:contraseña@localhost:5432/lou_barbershop
```

5. Inicializar la base de datos:

```bash
python migrations.py db init
python migrations.py db migrate -m "Iniciar base de datos"
python migrations.py db upgrade
```

6. Cargar datos iniciales:

```bash
flask init-db
```

## Ejecución

Para ejecutar la aplicación en modo desarrollo:

```bash
python run.py
```

O alternativamente:

```bash
flask --app app run
```

La aplicación estará disponible en `http://127.0.0.1:5000/`

## Estructura del Proyecto

- **app/**: Directorio principal de la aplicación
  - **models/**: Modelos de la base de datos
  - **routes/**: Rutas de la aplicación
  - **templates/**: Plantillas HTML
  - **static/**: Archivos estáticos (CSS, JS)
  - **forms/**: Formularios de la aplicación
  - **services/**: Servicios y lógica de negocio
- **migrations/**: Archivos de migración de la base de datos
- **requirements.txt**: Dependencias del proyecto
- **run.py**: Script para ejecutar la aplicación
- **migrations.py**: Script para gestionar migraciones de la base de datos

## Roles de Usuario

1. **Cliente**:
   - Puede registrarse e iniciar sesión
   - Puede ver y actualizar su perfil
   - Puede hacer reservas y ver su historial
   - Puede cancelar sus propias reservas

2. **Administrador**:
   - Puede gestionar todas las reservas
   - Puede administrar servicios y empleados
   - Puede bloquear horarios no disponibles
   - Puede ver estadísticas del sistema