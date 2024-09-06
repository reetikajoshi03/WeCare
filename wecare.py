# Import necessary libraries
from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'  

# MySQL database setup
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="abhi992744",
    database="wecaredb"
)
cursor = conn.cursor()

# Create users table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL
    )
''')

# Create users table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS help_requests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    name VARCHAR(255) NOT NULL,
    age INT NOT NULL,
    gender VARCHAR(10) NOT NULL,
    disease_name VARCHAR(255) NOT NULL,
    symptoms TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
    )
''')

# Create patients table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS patients(
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    name VARCHAR(255) NOT NULL,
    age INT NOT NULL,
    gender VARCHAR(10) NOT NULL,
    disease_name VARCHAR(255) NOT NULL,
    symptomps TEXT NOT NULL,
    hospital_name VARCHAR(255) NOT NULL,
    doc_name VARCHAR(255) NOT NULL,
    expenditure FLOAT NOT NULL,
    email VARCHAR(255) NOT NULL,
    remarks TEXT,
    rating int,
    FOREIGN KEY (user_id) REFERENCES users(id)
    )
''')

conn.commit()
conn.close()

# Route for the home page (index page)
@app.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))

    # Retrieve user details from the session
    username = session['username']

    return render_template('index.html', username=username)

# Route for user registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Handle user registration
        username = request.form['username']
        password = request.form['password']

        # Save user data to the database
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="abhi992744",
            database="wecaredb"
        )
        cursor = conn.cursor()
        
        # Check if the username is already taken
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            return render_template('register.html', message='Username already taken. Please choose another.')

        # Insert user data
        cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, password))

        conn.commit()

        cursor.execute('SELECT id FROM users WHERE username = %s', (username,))
        user_id = cursor.fetchone()[0]

        session['username'] = username
        session['user_id'] = user_id

        # Redirect to the login page after successful registration
        return redirect(url_for('login'))

    return render_template('register.html')

# Route for the login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Handle user login
        username = request.form['username']
        password = request.form['password']

        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="abhi992744",
            database="wecaredb"
            )
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
        user = cursor.fetchone()

        conn.close()

        if user:
            session['username'] = username  # Store username in session
            return redirect(url_for('index'))
        else:
            # Display an error message
            return render_template('login.html', message='Invalid username or password. Please try again.')
            
    return render_template('login.html')


# Route for logging out
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


# Route for entering patient information
@app.route('/enter_info', methods=['GET', 'POST'])
def enter_info():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="abhi992744",
        database="wecaredb"
    )
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM users WHERE username = %s', (username,))
    user_id = cursor.fetchone()[0]

    cursor.execute('SELECT id FROM patients WHERE user_id = %s', (user_id,))
    existing_patient_info = cursor.fetchone()
    conn.close()

    if existing_patient_info:
        # User has already entered patient details, redirect to a page indicating that
        return render_template('already_entered.html')

    if request.method == 'POST':
        # patient info
        username = session['username']
        name = request.form['name']
        age = int(request.form['age']) 
        gender = request.form['gender']
        disease_name = request.form['disease_name']
        symptomps = request.form['symptomps']
        hospital_name = request.form['hospital_name']
        doc_name = request.form['doc_name']
        expenditure = float(request.form['expenditure']) 
        email = request.form['email']
        remarks = request.form['remarks']

        # Save patient data to the database
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="abhi992744",
            database="wecaredb"
        )
        cursor = conn.cursor()

        # Get user ID based on the username
        cursor.execute('SELECT id FROM users WHERE username = %s', (username,))
        user_id = cursor.fetchone()[0]

        # Insert patient data with correct placeholders
        cursor.execute('''
            INSERT INTO patients (user_id, name, age, gender, disease_name, symptomps, hospital_name, doc_name, expenditure, email, remarks)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', (user_id, name, age, gender, disease_name, symptomps, hospital_name, doc_name, expenditure, email, remarks))

        conn.commit()
        conn.close()
        
        return render_template('entry_success.html')

    return render_template('enter_info.html')


# Route for patient details
@app.route('/patientdetails')
def patient_details():
    if 'username' not in session:
        return redirect(url_for('login'))

    # Fetch patient details from the database
    username = session['username']
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="abhi992744",
        database="wecaredb"
    )
    cursor = conn.cursor()

    # Get user ID based on the username
    cursor.execute('SELECT id FROM users WHERE username = %s', (username,))
    user_id = cursor.fetchone()[0]

    # Fetch patient details for the user
    cursor.execute('SELECT * FROM patients WHERE user_id = %s', (user_id,))
    patient_details = cursor.fetchone()

    conn.close()

    return render_template('patientdetails.html', patient_details=patient_details)


#get user id
def get_user_id(username):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="abhi992744",
        database="wecaredb"
    )
    cursor = conn.cursor()

    # Get user ID based on the username
    cursor.execute('SELECT id FROM users WHERE username = %s', (username,))
    user_id = cursor.fetchone()[0]

    conn.close()
    return user_id

def save_help_request(user_id, name, age, gender, disease_name, symptoms):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="abhi992744",
        database="wecaredb"
    )
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO help_requests (user_id, name, age, gender, disease_name, symptoms)
        VALUES (%s, %s, %s, %s, %s, %s)
    ''', (user_id, name, age, gender, disease_name, symptoms))
    conn.commit()
    conn.close()

def get_matching_patient_details(disease_name):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="abhi992744",
        database="wecaredb"
    )
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM patients WHERE disease_name = %s', (disease_name,))
    matching_patient_details = cursor.fetchall()
    conn.close()
    return matching_patient_details





# Route for seeking help
@app.route('/seek_help', methods=['GET', 'POST'])
def seek_help():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']

    if request.method == 'POST':
        name = request.form['name']
        age = int(request.form['age'])
        gender = request.form['gender']
        disease_name = request.form['disease_name']
        symptoms = request.form['symptoms']

        # Get user ID based on the username
        user_id = get_user_id(username)

        save_help_request(user_id, name, age, gender, disease_name, symptoms)

        # Perform matching
        matching_patient_details = get_matching_patient_details(disease_name)

        return render_template('seek_help_result.html', matching_patient_details=matching_patient_details)

    return render_template('seek_help.html')




if __name__ == '__main__':
    app.run(debug=True)
