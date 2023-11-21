from flask import Flask, render_template, request, redirect, url_for, jsonify, flash, session
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
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:12345@localhost/assignment'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'jwt_secret_key' 
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)  
app.config['SECRET_KEY'] = 'secret_key'  
jwt = JWTManager(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

db = SQLAlchemy(app)

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), nullable=False)
    given_name = db.Column(db.String(255), nullable=False)
    surname = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(255))
    phone_number = db.Column(db.String(20))
    profile_description = db.Column(db.Text)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable = False)

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



login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

headers = {'Content-Type': 'application/json'}

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/', methods=['GET'])
def login_page():
    return render_template('login.html')

@app.route('/', methods=['POST'])
def login_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user and user.password == password:
           
            session['user_id'] = user.user_id
            session['role'] = user.role
            access_token = create_access_token(identity=user.user_id)

            if user.role == 'caregiver':
                return redirect(url_for('caregiver_dashboard'))
            elif user.role == 'family':
                return redirect(url_for('family_dashboard'))

        else:
            return jsonify({'status': 'error', 'message': 'Invalid email or password'}), 401

@app.route('/caregiver_dashboard')
def caregiver_dashboard():
    if 'user_id' in session and session.get('role') == 'caregiver':
        user_id = session.get('user_id')
        user = User.query.get(user_id)
        return render_template('caregiver_dashboard.html', user=user)
    else:
        return redirect(url_for('login_page'))

@app.route('/family_dashboard')
def family_dashboard():
    if 'user_id' in session and session.get('role') == 'family':
        user_id = session.get('user_id')
        user = User.query.get(user_id)
        jobs = Job.query.filter_by(member_user_id=user_id).all()
        return render_template('family_dashboard.html', user=user, jobs=jobs)
    else:
        return redirect(url_for('login_page'))

@app.route('/protected', methods=['GET'])
@login_required
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


@app.route('/register', methods=['GET'])
def registration_page():
    return render_template('register.html')


@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username', None)
    password = request.form.get('password', None)
    given_name = request.form.get('name', None)
    surname = request.form.get('surname', None)
    city = request.form.get('city', None)
    phone_number = request.form.get('phone_number', None)
    profile_description = request.form.get('profile_description', None)
    role = request.form.get('role', None)

    if not username or not password or not given_name or not surname or not city or not phone_number or not profile_description or not role:
        return jsonify({'message': 'All fields are required'}), 400

    existing_user = User.query.filter_by(email=username).first()

    if existing_user:
        return jsonify({'message': 'User already exists'}), 409

    new_user = User(email=username, password=password, given_name=given_name, surname=surname, city=city, phone_number=phone_number, profile_description=profile_description, role=role)

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('login_page'))

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

        if user.role == 'caregiver':
            return redirect(url_for('caregiver_dashboard'))
        elif user.role == 'family':
            return redirect(url_for('family_dashboard'))

    return render_template('update.html', user=user)


@app.route('/create_job', methods=['GET', 'POST'])
def create_job():
    if request.method == 'POST':
        user_id = session.get('user_id')
        member = User.query.get(user_id)

        new_job = Job(
            member_user_id=user_id,
            required_caregiving_type=request.form['required_caregiving_type'],
            other_requirements=request.form['other_requirements'],
            date_posted=datetime.now().date()
        )

        db.session.add(new_job)
        db.session.commit()

        flash("Job created successfully", "success")
        return redirect(url_for('family_dashboard'))

    return render_template('create_job.html')

@app.route('/update_job/<int:job_id>', methods=['GET', 'POST'])
def update_job(job_id):
    job = Job.query.get(job_id)

    if not job:
        flash("Job not found", "error")
        return redirect(url_for('family_dashboard'))

    if request.method == 'POST':
        job.required_caregiving_type = request.form['required_caregiving_type']
        job.other_requirements = request.form['other_requirements']
        job.date_posted = datetime.now().date()

        db.session.commit()

        flash("Job updated successfully", "success")
        return redirect(url_for('family_dashboard'))

    return render_template('update_job.html', job=job)

@app.route('/delete_job/<int:job_id>', methods=['GET'])
def delete_job(job_id):
    job = Job.query.get(job_id)

    if not job:
        flash("Job not found", "error")
        return redirect(url_for('family_dashboard'))

    db.session.delete(job)
    db.session.commit()

    flash("Job deleted successfully", "success")
    return redirect(url_for('family_dashboard'))


@app.route('/logout')
def logout_user():
    session.pop('user_id', None)
    return redirect(url_for('login_page'))

if __name__ == '__main__':
    app.run(debug=True)
