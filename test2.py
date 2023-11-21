from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from datetime import datetime, timedelta
from sqlalchemy import MetaData, create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:12345@localhost:3306/assignment'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # Change this to a secret key of your choice
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)  # Adjust token expiration as needed
app.config['SECRET_KEY'] = 'your_secret_key'  # Change this to a secret key of your choice
jwt = JWTManager(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

DATABASE_URL = "mysql+mysqlconnector://root:12345@localhost/assignment"
engine = create_engine(DATABASE_URL)
metadata = MetaData()
metadata.reflect(engine)
Base = automap_base(metadata=metadata)
Base.prepare()
# Create a sessionmaker object


Session = sessionmaker(bind=engine)
# Assign the automapped classes to variables to be imported in other modules
User = Base.classes.USER
Caregiver = Base.classes.CAREGIVER
Member = Base.classes.MEMBER
Address = Base.classes.ADDRESS
Job = Base.classes.JOB
JobApplication = Base.classes.JOB_APPLICATION
Appointment = Base.classes.APPOINTMENT

db = SQLAlchemy(app)

# Define models
class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), nullable=False)
    given_name = db.Column(db.String(255), nullable=False)
    surname = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(255))
    phone_number = db.Column(db.String(20))
    profile_description = db.Column(db.Text)
    password = db.Column(db.String(255), nullable=False)

class Caregiver(db.Model):
    caregiver_user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)
    photo = db.Column(db.LargeBinary)
    gender = db.Column(db.String(20))
    caregiving_type = db.Column(db.String(255))
    hourly_rate = db.Column(db.Integer)
    user = db.relationship('User', backref='caregiver', uselist=False)

class Member(db.Model):
    member_user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)
    house_rules = db.Column(db.Text)
    user = db.relationship('User', backref='member', uselist=False)

class Address(db.Model):
    member_user_id = db.Column(db.Integer, db.ForeignKey('member.member_user_id'), primary_key=True)
    house_number = db.Column(db.Integer)
    street = db.Column(db.String(255))
    town = db.Column(db.String(255))
    member = db.relationship('Member', backref='address', uselist=False)

class Job(db.Model):
    job_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    member_user_id = db.Column(db.Integer, db.ForeignKey('member.member_user_id'))
    required_caregiving_type = db.Column(db.String(255))
    other_requirements = db.Column(db.Text)
    date_posted = db.Column(db.Date)
    member = db.relationship('Member', backref='jobs')

class JobApplication(db.Model):
    caregiver_user_id = db.Column(db.Integer, db.ForeignKey('caregiver.caregiver_user_id'), primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('job.job_id'), primary_key=True)
    date_applied = db.Column(db.Date)

class Appointment(db.Model):
    appointment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    caregiver_user_id = db.Column(db.Integer, db.ForeignKey('caregiver.caregiver_user_id'))
    member_user_id = db.Column(db.Integer, db.ForeignKey('member.member_user_id'))
    appointment_date = db.Column(db.Date)
    appointment_time = db.Column(db.Time)
    work_hours = db.Column(db.String(50))
    status = db.Column(db.String(50))


from main import db
db.create_all()

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
headers = {'Content-Type': 'application/json'}

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users=users)

@app.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        print(f"Received email: {email}")
        print(f"Received password: {password}")

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            access_token = create_access_token(identity=user.user_id)
            return jsonify(access_token=access_token, user_id=user.user_id)
        else:
            return jsonify({'status': 'error', 'message': 'Invalid email or password'}), 401



@app.route('/protected', methods=['GET'])
@login_required
def protected():
    # Access the identity of the current user with current_user.id
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


@app.route('/register', methods=['GET'])
def registration_page():
    return render_template('register.html')


@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username', None)
    password = request.form.get('password', None)

    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400

    # Hash the password before storing it in the database
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

    # Check if the user already exists
    existing_user = User.query.filter_by(email=username).first()

    if existing_user:
        return jsonify({'message': 'User already exists'}), 409

    # Create a new user with the hashed password
    new_user = User(email=username, password=hashed_password)

    # Add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/update/<int:user_id>', methods=['GET', 'POST'])
def update_user(user_id):
    user = User.query.get(user_id)

    if request.method == 'POST':
        user.email = request.form['email']
        user.given_name = request.form['given_name']
        user.surname = request.form['surname']
        user.city = request.form['city']
        user.phone_number = request.form['phone_number']
        user.profile_description = request.form['profile_description']

        db.session.commit()

        return redirect(url_for('index'))

    return render_template('update.html', user=user)

@app.route('/delete/<int:user_id>')
def delete_user(user_id):
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect(url_for('index'))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
