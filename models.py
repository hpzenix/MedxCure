from app import app
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy(app)


# ----- ADMIN -----
class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False, unique=True)
    passhash = db.Column(db.String(256), nullable=False)
    email_id = db.Column(db.String(100), nullable=False, unique=True)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)



# ----- DOCTORS ------
class Doctor(db.Model):
    __tablename__ = 'doctors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    email_id = db.Column(db.String(100), nullable=False, unique=True)
    username = db.Column(db.String(64), nullable=False, unique=True)
    passhash = db.Column(db.String(256), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    mobile_number = db.Column(db.String(15), nullable=False, unique=True)
    qualification = db.Column(db.String(100), nullable=False)
    specialization = db.Column(db.String(100), nullable=False)
    experience_years = db.Column(db.Integer, default=0)
    status = db.Column(db.String(20), nullable=False, default='active')  # active/inactive/blacklisted

    # Relationship
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)

    # A doctor has many availabilities and appointments
    availabilities = db.relationship('DoctorAvailability', backref='doctor', lazy=True)
    appointments = db.relationship('Appointment', backref='doctor', lazy=True)

    
    
    
# ----- DOCTOR AVAILABILITY -----
class DoctorAvailability(db.Model):
    __tablename__ = 'doctor_availability'

    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    morning_start = db.Column(db.Time, nullable=True)
    morning_end = db.Column(db.Time, nullable=True)
    evening_start = db.Column(db.Time, nullable=True)
    evening_end = db.Column(db.Time, nullable=True)
    is_available_morning = db.Column(db.Boolean, default=False)
    is_available_evening = db.Column(db.Boolean, default=False)
   


# ----- DEPARTMENTS -----
class Department(db.Model):
    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)

    # Relationship: one department has many doctors
    doctors = db.relationship('Doctor', backref='department', lazy=True)
    appointments = db.relationship('Appointment', backref='department', lazy=True)


# ----- PATIENTS -----
class Patient(db.Model):
    __tablename__ = 'patients'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    email_id = db.Column(db.String(100), nullable=False, unique=True)
    username = db.Column(db.String(64), nullable=False, unique=True)
    passhash = db.Column(db.String(256), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    height_cm = db.Column(db.Float, nullable=False)
    weight_kg = db.Column(db.Float, nullable=False)
    dob = db.Column(db.Date, nullable=False)
    mobile_number = db.Column(db.String(15), nullable=False, unique=True)
    blood_group = db.Column(db.String(5), nullable=False)
    allergies = db.Column(db.String(256), nullable=True)
    medical_history = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), nullable=False, default='active')  # active/blacklisted

    # Relationship: one patient has many appointments
    appointments = db.relationship('Appointment', backref='patient', lazy=True)


# ----- APPOINTMENTS -----
class Appointment(db.Model):
    __tablename__ = 'appointments'

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    appointment_date = db.Column(db.DateTime, nullable=False)
    availability_id = db.Column(db.Integer, db.ForeignKey('doctor_availability.id'))
    status = db.Column(db.String(20), nullable=False, default='Booked')  # Booked, Canceled, Completed
    appointment_mode = db.Column(db.String(20), nullable=False)  # Online / In-person

    # One appointment has one treatment
    treatment = db.relationship('Treatment', backref='appointment', uselist=False)


# ----- TREATMENTS -----
class Treatment(db.Model):
    __tablename__ = 'treatments'

    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointments.id'), nullable=False)
    diagnosis = db.Column(db.Text, nullable=False)
    prescriptions = db.Column(db.Text, nullable=True)
    notes = db.Column(db.Text, nullable=True)
    follow_up_date = db.Column(db.Date, nullable=True)


# ----- INITIAL SETUP -----
with app.app_context():
    db.create_all()

    # Create a default admin if not exists
    admin = Admin.query.filter_by(is_admin=True).first()
    if not admin:
        password_hash = generate_password_hash('master@admin10')
        admin = Admin(
            username='masteradmin',
            email_id='masteradmin@example.com',
            passhash=password_hash,
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()
    