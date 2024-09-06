import random

# Sample data for names and diseases
names = ["Abhishek", "Reetika", "Garv", "Kajal", "Raj", "Rahul"]
diseases = ["Flu", "Cancer", "Diabetes", "Heart Disease", "COVID-19","Lung Cancer"]

# Generate INSERT statements for patients
patient_insert_statements = []
for user_id in range(1,201):
    name = random.choice(names)
    age = random.randint(18, 80)
    gender = random.choice(['Male', 'Female'])
    disease_name = random.choice(diseases)
    symptomps = f"Symptoms for {disease_name}"
    hospital_name = f"Hospital for {disease_name}"
    doc_name = random.choice(names)
    expenditure = round(random.uniform(100.0, 5000.0), 2)
    email = f"{name.replace(' ', '.').lower()}@example.com"
    remarks = f"Remarks for {disease_name}"
    patient_insert_statements.append(f"INSERT INTO patients (user_id, name, age, gender, disease_name, symptomps, "
                                     f"hospital_name, doc_name, expenditure, email, remarks) "
                                     f"VALUES ({user_id}, '{name}', {age}, '{gender}', '{disease_name}', '{symptomps}', "
                                     f"'{hospital_name}', '{doc_name}', {expenditure}, '{email}', '{remarks}');")

# Print the generated SQL statements
for statement in patient_insert_statements:
    print(statement)
