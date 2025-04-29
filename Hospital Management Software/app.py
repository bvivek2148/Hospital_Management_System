from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Required for flash messages and sessions

# Database initialization
def init_db():
    conn = sqlite3.connect('hospital.db')
    c = conn.cursor()
    
    # Create patients table
    c.execute('''CREATE TABLE IF NOT EXISTS patients
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  age INTEGER,
                  gender TEXT,
                  phone TEXT,
                  address TEXT)''')
    
    # Create doctors table
    c.execute('''CREATE TABLE IF NOT EXISTS doctors
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  specialization TEXT,
                  phone TEXT)''')
    
    # Create appointments table with status column
    c.execute('''CREATE TABLE IF NOT EXISTS appointments
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  patient_id INTEGER,
                  doctor_id INTEGER,
                  date TEXT,
                  time TEXT,
                  status TEXT DEFAULT 'Scheduled',
                  FOREIGN KEY (patient_id) REFERENCES patients (id),
                  FOREIGN KEY (doctor_id) REFERENCES doctors (id))''')
    
    # Create admin table with default credentials
    c.execute('''CREATE TABLE IF NOT EXISTS admin
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT UNIQUE NOT NULL,
                  password TEXT NOT NULL)''')
    
    # Insert default admin if not exists
    c.execute("INSERT OR IGNORE INTO admin (username, password) VALUES (?, ?)", 
             ('cmrtc', 'cmrtc'))
    
    conn.commit()
    conn.close()

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            flash('Please log in first.')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Routes
@app.route('/')
def index():
    conn = sqlite3.connect('hospital.db')
    c = conn.cursor()
    
    # Get today's appointments
    c.execute("""
        SELECT a.id, p.name as patient_name, d.name as doctor_name, a.date, a.time
        FROM appointments a
        JOIN patients p ON a.patient_id = p.id
        JOIN doctors d ON a.doctor_id = d.id
        WHERE a.date = date('now')
    """)
    appointments = c.fetchall()
    conn.close()
    
    return render_template('index.html', appointments=appointments)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = sqlite3.connect('hospital.db')
        c = conn.cursor()
        c.execute("SELECT * FROM admin WHERE username=? AND password=?", 
                 (username, password))
        user = c.fetchone()
        conn.close()
        
        if user:
            session['logged_in'] = True
            flash('Login successful!')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials!')
    return render_template('login.html')

@app.route('/register_patient', methods=['GET', 'POST'])
@login_required
def register_patient():
    conn = sqlite3.connect('hospital.db')
    c = conn.cursor()
    
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        phone = request.form['phone']
        address = request.form['address']
        
        c.execute("INSERT INTO patients (name, age, gender, phone, address) VALUES (?, ?, ?, ?, ?)",
                 (name, age, gender, phone, address))
        conn.commit()
        flash('Patient registered successfully!')
    
    # Fetch all patients for display
    c.execute("SELECT * FROM patients")
    patients = c.fetchall()
    conn.close()
    
    return render_template('register_patient.html', patients=patients)

@app.route('/add_doctor', methods=['GET', 'POST'])
@login_required
def add_doctor():
    conn = sqlite3.connect('hospital.db')
    c = conn.cursor()
    
    if request.method == 'POST':
        name = request.form['name']
        specialization = request.form['specialization']
        phone = request.form['phone']
        
        c.execute("INSERT INTO doctors (name, specialization, phone) VALUES (?, ?, ?)",
                 (name, specialization, phone))
        conn.commit()
        flash('Doctor added successfully!')
    
    # Fetch all doctors for display
    c.execute("SELECT * FROM doctors")
    doctors = c.fetchall()
    conn.close()
    
    return render_template('add_doctor.html', doctors=doctors)

@app.route('/delete_patient/<int:id>')
@login_required
def delete_patient(id):
    conn = sqlite3.connect('hospital.db')
    c = conn.cursor()
    c.execute("DELETE FROM patients WHERE id=?", (id,))
    conn.commit()
    conn.close()
    flash('Patient deleted successfully!')
    return redirect(url_for('register_patient'))

@app.route('/delete_doctor/<int:id>')
@login_required
def delete_doctor(id):
    conn = sqlite3.connect('hospital.db')
    c = conn.cursor()
    c.execute("DELETE FROM doctors WHERE id=?", (id,))
    conn.commit()
    conn.close()
    flash('Doctor deleted successfully!')
    return redirect(url_for('add_doctor'))

@app.route('/appointments', methods=['GET', 'POST'])
@login_required
def appointments():
    conn = sqlite3.connect('hospital.db')
    c = conn.cursor()
    
    if request.method == 'POST':
        patient_id = request.form['patient_id']
        doctor_id = request.form['doctor_id']
        date = request.form['date']
        time = request.form['time']
        
        c.execute("INSERT INTO appointments (patient_id, doctor_id, date, time) VALUES (?, ?, ?, ?)",
                 (patient_id, doctor_id, date, time))
        conn.commit()
        flash('Appointment scheduled successfully!')
        
    # Get all appointments with patient and doctor names
    c.execute("""
        SELECT a.id, p.name as patient_name, d.name as doctor_name, a.date, a.time
        FROM appointments a
        JOIN patients p ON a.patient_id = p.id
        JOIN doctors d ON a.doctor_id = d.id
    """)
    appointments = c.fetchall()
    
    # Get all patients and doctors for the dropdown
    c.execute("SELECT id, name FROM patients")
    patients = c.fetchall()
    
    c.execute("SELECT id, name, specialization FROM doctors")
    doctors = c.fetchall()
    
    conn.close()
    
    return render_template('appointments.html', 
                         appointments=appointments,
                         patients=patients,
                         doctors=doctors)

@app.route('/dashboard')
@login_required
def dashboard():
    conn = sqlite3.connect('hospital.db')
    c = conn.cursor()
    
    # Get statistics
    c.execute("SELECT COUNT(*) FROM patients")
    total_patients = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM doctors")
    total_doctors = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM appointments WHERE date = date('now')")
    today_appointments = c.fetchone()[0]
    
    # Updated departments data with actual counts from database
    departments = [
        {
            'name': 'Cardiology',
            'doctors': c.execute("SELECT COUNT(*) FROM doctors WHERE specialization='Cardiology'").fetchone()[0],
            'patients': 12,
            'image': 'cardiology.jpg'
        },
        {
            'name': 'Orthopedics',
            'doctors': c.execute("SELECT COUNT(*) FROM doctors WHERE specialization='Orthopedics'").fetchone()[0],
            'patients': 15,
            'image': 'orthopedics.jpg'
        },
        {
            'name': 'Neurology',
            'doctors': c.execute("SELECT COUNT(*) FROM doctors WHERE specialization='Neurology'").fetchone()[0],
            'patients': 8,
            'image': 'neurology.jpg'
        },
        {
            'name': 'Pediatrics',
            'doctors': c.execute("SELECT COUNT(*) FROM doctors WHERE specialization='Pediatrics'").fetchone()[0],
            'patients': 20,
            'image': 'pediatrics.jpg'
        }
    ]
    
    # Get recent activities
    activities = [
        {
            'icon': 'fas fa-user-plus',
            'description': f'Total Patients: {total_patients}',
            'time': 'Current Count'
        },
        {
            'icon': 'fas fa-user-md',
            'description': f'Total Doctors: {total_doctors}',
            'time': 'Current Count'
        },
        {
            'icon': 'fas fa-calendar-check',
            'description': f'Today\'s Appointments: {today_appointments}',
            'time': 'Today'
        }
    ]
    
    # Get today's appointments with modified query
    c.execute("""
        SELECT 
            a.id, 
            p.name as patient_name, 
            d.name as doctor_name, 
            a.date, 
            a.time
        FROM appointments a
        JOIN patients p ON a.patient_id = p.id
        JOIN doctors d ON a.doctor_id = d.id
        WHERE date(a.date) = date('now')
    """)
    appointments = c.fetchall()
    
    stats = {
        'total_patients': total_patients,
        'total_doctors': total_doctors,
        'today_appointments': today_appointments,
        'available_beds': 50
    }
    
    conn.close()
    
    return render_template('dashboard.html', 
                         stats=stats,
                         appointments=appointments,
                         departments=departments,
                         activities=activities)

@app.route('/reset_db')
def reset_db():
    import os
    
    # Close any open connections
    try:
        conn = sqlite3.connect('hospital.db')
        conn.close()
    except:
        pass
        
    # Delete the database file
    if os.path.exists('hospital.db'):
        os.remove('hospital.db')
    
    # Reinitialize the database
    init_db()
    flash('Database has been reset successfully!')
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully!')
    return redirect(url_for('login'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)