🏥** Hospital Management System (Flask + PostgreSQL)**

This project is a **role-based hospital management web application** built using **Flask, Jinja, and PostgreSQL**, aimed at simplifying hospital operations through digital automation.
It provides separate dashboards and features for **Admins**, **Doctors**, and **Patients**, ensuring secure and efficient workflow management.

### 🔹 Overview

The system manages hospital activities such as **appointment scheduling**, **doctor availability**, **patient registration**, and **treatment tracking**. Each user type has access to specific functionalities based on their role, ensuring clear separation of responsibilities.

* **Admins** can manage doctors, patients, and appointments, monitor hospital statistics, and handle overall data maintenance.
* **Doctors** can view their daily schedules, mark appointments as completed or cancelled, and record diagnosis and prescriptions for each patient.
* **Patients** can register, search for doctors by specialization, book or reschedule appointments, and view their complete medical history.

The application enforces **role-based authentication**, prevents double bookings, and maintains comprehensive treatment records for every visit, improving both efficiency and transparency in hospital management.

### 💻 Tech Stack

* **Backend:** Flask (Python)
* **Frontend:** Jinja2 Templates, HTML, CSS
* **Database:** PostgreSQL with SQLAlchemy ORM
* **Authentication:** Role-based access (Admin, Doctor, Patient)

