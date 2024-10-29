from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate  # Importa Flask-Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token

app = Flask(__name__)
app.secret_key = 'porta'

# Configura la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://ugk2nsgl77xe7w0j:qPSKJQALkY2eQP4gWzhf@bikibggurwnmevjbgtwu-mysql.services.clever-cloud.com:3306/bikibggurwnmevjbgtwu'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JWT_SECRET_KEY"] = "porta"

db = SQLAlchemy(app)
migrate = Migrate(app, db)  # Inicializa Flask-Migrate
jwt = JWTManager(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    if request.method == 'POST':
        nombre = request.form.get('nombre_sign')
        contraseña = request.form.get('password_sign')

        if not nombre or not contraseña:
            flash('Se necesitan nombre y contraseña')
            return redirect(url_for('sign_in'))

        if User.query.filter_by(username=nombre).first():
            flash('El usuario ya existe. Por favor, elija otro nombre de usuario.')
            return redirect(url_for('sign_in'))

        hashed_password = generate_password_hash(contraseña, method='sha256')
        new_user = User(username=nombre, email=f'{nombre}@example.com', password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('log_in'))

    return render_template('sign_in.html')

@app.route('/log_in', methods=['GET', 'POST'])
def log_in():
    if request.method == 'POST':
        nombres = request.form.get('nombres')
        password = request.form.get('password')

        if not nombres or not password:
            error = "Por favor, completa ambos campos."
            return render_template('log_in.html', error=error)

        user = User.query.filter_by(username=nombres).first()
        if user and check_password_hash(user.password, password):
            session['nombres'] = nombres
            access_token = create_access_token(identity={'username': user.username})
            return redirect(url_for('home'))

        error = "Usuario o contraseña incorrectos."
        return render_template('log_in.html', error=error)

    return render_template('log_in.html')

if __name__ == '__main__':
    app.run(debug=True)
