from flask import render_template, request, redirect, url_for, flash, session
from app import app
from models import db, User, Patient, Doctor
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

@app.route('/')
def homepage():
    return render_template('homepage.html')


# login
@app.route('/login')
def login():
    return render_template('authentication/login.html')

@app.route('/login', methods=['POST'])
def login_post():
    email_id = request.form.get('email_id')
    password = request.form.get('password')

    if not email_id or not password:
        flash('Please enter your email and password.', 'warning')
        return redirect(url_for('login'))
    
    user = User.query.filter_by(email_id=email_id).first()
    
    if user and check_password_hash(user.passhash, password):
        session['id'] = user.id
        session['role'] = user.role
        flash('Login successful.', 'success')
        return redirect(url_for('dashboard'))
    else:
        flash('Invalid email or password.', 'danger')
        return redirect(url_for('login'))



# signup
@app.route('/signup')
def signup():
    return render_template('authentication/signup.html')

@app.route('/signup', methods=['POST'])
def signup_post():
    name = request.form.get('name')
    username = request.form.get('username')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    email_id = request.form.get('email_id')
    mobile_number = request.form.get('mobile_number')
    gender = request.form.get('gender')
    dob = request.form.get('dob')
    blood_group = request.form.get('blood_group')
    height = request.form.get('height')
    weight = request.form.get('weight')
    medical_history = request.form.get('medical_history')
    allergies = request.form.get('allergies')
    
    if not name or not username or not password or not confirm_password or not email_id or not mobile_number or not gender or not dob or not blood_group or not height or not weight or not medical_history or not allergies:
        return redirect(url_for('signup'))
    
    if password != confirm_password:
        flash('Passwords do not match.', 'danger')
        return redirect(url_for('signup'))

    existing_user = User.query.filter((User.username == username) | (User.email_id == email_id)).first()
    if existing_user:
        flash('Username or Email ID already exists.', 'danger')
        return redirect(url_for('signup'))
    
    password_hash = generate_password_hash(password)
    new_user = User(username=username, passhash=password_hash, email_id=email_id, role='PATIENT')
    db.session.add(new_user)
    db.session.flush()

    dob = datetime.strptime(dob, '%Y-%m-%d').date()
    height_cm = float(height)
    weight_kg = float(weight)
            
    new_patient = Patient(name=name, gender=gender, dob=dob, mobile_number=mobile_number, blood_group=blood_group, height=height_cm, weight=weight_kg, medical_history=medical_history, allergies=allergies, status='active', user_id=new_user.id)
    db.session.add(new_patient)
    db.session.commit()
    
    flash('Signup successful. Please log in.', 'success')
    return redirect(url_for('login'))



    
