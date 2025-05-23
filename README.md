# Hospital Management System

A comprehensive web-based Hospital Management System built with Flask, SQLite, and Bootstrap. This system helps manage patients, doctors, appointments, and hospital departments efficiently.

## Features

- **User Authentication**
  - Secure admin login system
  - Default credentials: Username: `cmrtc`, Password: `cmrtc`

- **Patient Management**
  - Register new patients
  - Store patient details (name, age, gender, contact info)
  - View all registered patients
  - Delete patient records

- **Doctor Management**
  - Add new doctors
  - Manage doctor specializations
  - View all registered doctors
  - Delete doctor records

- **Appointment System**
  - Schedule new appointments
  - View today's appointments
  - Track appointment status
  - Link patients with doctors

- **Dashboard**
  - Overview of hospital statistics
  - Department-wise distribution
  - Today's appointment list
  - Available beds counter
  - Recent activities tracker

## Technical Stack

- **Backend**: Python Flask
- **Database**: SQLite3
- **Frontend**: Bootstrap 5, Font Awesome
- **Security**: Session-based authentication

## Project Structure

```plaintext
Hospital Management Software/
├── app.py                 # Main application file
├── hospital.db           # SQLite database
├── static/              # Static files (CSS, JS)
│   └── style.css
└── templates/           # HTML templates
    ├── index.html
    ├── login.html
    ├── dashboard.html
    ├── register_patient.html
    ├── add_doctor.html
    └── appointments.html


## Installation & Setup
1. Ensure Python is installed on your system
2. Clone the repository
3. Install required dependencies:
         pip install flask
4. Run the application:
         python app.py
5. Access the application at http://localhost:5000


## Database Schema
The system uses SQLite with the following main tables:

### Patients Table
- patient_id (Primary Key)
- name (Text)
- age (Integer)
- gender (Text)
- phone (Text)
- address (Text)
- registration_date (DateTime)

### Doctors Table
- doctor_id (Primary Key)
- name (Text)
- specialization (Text)
- phone (Text)
- email (Text)
- status (Text)

### Appointments Table
- appointment_id (Primary Key)
- patient_id (Foreign Key)
- doctor_id (Foreign Key)
- appointment_date (DateTime)
- status (Text)
- description (Text)

### Admin Table
- admin_id (Primary Key)
- username (Text)
- password (Text)

## Security Features
1. Authentication
   - Secure password hashing
   - Session-based authentication
   - Login required decorator for protected routes
2. Data Protection
   - SQL injection prevention through parameterized queries
   - CSRF protection for forms
   - Secure session management
3. Access Control
   - Role-based access control
   - Protected admin routes
   - Session timeout management


## Usage
1. Initial Setup
   - Launch the application
   - Log in using admin credentials
   - Set up departments and basic configurations
2. Managing Patients
   - Click "Register Patient" to add new patients
   - View patient list in the dashboard
   - Update or delete patient records as needed
3. Doctor Management
   - Add new doctors with their specializations
   - Manage doctor availability
   - View doctor schedules
4. Appointment Handling
   - Create new appointments
   - Select patient and doctor
   - Choose appointment date and time
   - Track appointment status
5. Dashboard Navigation
   - Monitor daily statistics
   - View upcoming appointments
   - Check bed availability
   - Access quick actions
   
## Contributing
1. Fork the repository
2. Create a new branch ( git checkout -b feature/improvement )
3. Make your changes
4. Commit your changes ( git commit -am 'Add new feature' )
5. Push to the branch ( git push origin feature/improvement )
6. Create a Pull Request
