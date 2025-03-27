from pymongo import MongoClient
from datetime import datetime , timedelta

# Database connection 
def connect_to_database():
    try:
        client = MongoClient('mongodb://localhost:27017/')
        # Test the connection
        client.admin.command('ping')
        db = client['medical_service']
        print("Successfully connected to MongoDB")
        return db
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

# Add patients from keyboard 
def add_patients(db):
    patients_col = db['patients']
    
    for i in range(3):
        print(f"\nEnter information for patient #{i+1}:")
        full_name = input("Full name: ")
        date_of_birth = input("Date of birth (DD-MM-YYYY): ")
        gender = input("Gender (Male/Female/Other): ")
        address = input("Address: ")
        phone_number = input("Phone number: ")
        email = input("Email: ")
        
        try:
            patient_data = {
                "full_name": full_name,
                "date_of_birth": datetime.strptime(date_of_birth, "%d-%m-%Y"),
                "gender": gender,
                "address": address,
                "phone_number": phone_number,
                "email": email
            }
            
            result = patients_col.insert_one(patient_data)
            print(f"Added patient {full_name} with ID: {result.inserted_id}")
        except ValueError as e:
            print(f"Date format error: {e}. Please use DD-MM-YYYY format.")
            continue

# Add doctors from keyboard 
def add_doctors(db):
    doctors_col = db['doctors']
    
    for i in range(5):
        print(f"\nEnter information for doctor #{i+1}:")
        full_name = input("Full name: ")
        specialization = input("Specialization: ")
        phone_number = input("Phone number: ")
        email = input("Email: ")
        years_of_experience = int(input("Years of experience: "))
        
        doctor_data = {
            "full_name": full_name,
            "specialization": specialization,
            "phone_number": phone_number,
            "email": email,
            "years_of_experience": years_of_experience
        }
        
        result = doctors_col.insert_one(doctor_data)
        print(f"Added doctor {full_name} with ID: {result.inserted_id}")

# Add appointments 
def add_appointments(db):
    patients_col = db['patients']
    doctors_col = db['doctors']
    appointments_col = db['appointments']
    
    # Show patient list
    print("\nPatient list:")
    patients = list(patients_col.find())
    for idx, patient in enumerate(patients, 1):
        print(f"{idx}. {patient['full_name']} (ID: {patient['_id']})")
    
    # Show doctor list
    print("\nDoctor list:")
    doctors = list(doctors_col.find())
    for idx, doctor in enumerate(doctors, 1):
        print(f"{idx}. {doctor['full_name']} - {doctor['specialization']} (ID: {doctor['_id']})")
    
    for i in range(3):
        print(f"\nCreate appointment #{i+1}:")
        
        # Select patient
        patient_idx = int(input("Select patient number: ")) - 1
        patient_id = patients[patient_idx]['_id']
        
        # Select doctor
        doctor_idx = int(input("Select doctor number: ")) - 1
        doctor_id = doctors[doctor_idx]['_id']
        
        # Get optional appointment details
        appointment_date = input("Appointment date (optional, format DD-MM-YYYY HH:MM): ")
        reason = input("Reason (optional): ")
        
        appointment_data = {
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "status": "pending",
            "created_at": datetime.now()
        }
        
        # Add date if provided
        if appointment_date:
            try:
                appointment_data["appointment_date"] = datetime.strptime(appointment_date, "%d-%m-%Y %H:%M")
            except ValueError:
                print("Warning: Invalid date format, saving without appointment date")
        
        # Add reason if provided
        if reason:
            appointment_data["reason"] = reason
            
        result = appointments_col.insert_one(appointment_data)
        print(f"Created appointment ID: {result.inserted_id}")

# Generate report 
def generate_report(db):
    pipeline = [
        {
            "$lookup": {
                "from": "patients",
                "localField": "patient_id",
                "foreignField": "_id",
                "as": "patient"
            }
        },
        {
            "$lookup": {
                "from": "doctors",
                "localField": "doctor_id",
                "foreignField": "_id",
                "as": "doctor"
            }
        },
        {
            "$unwind": "$patient"
        },
        {
            "$unwind": "$doctor"
        },
        {
            "$project": {
                "_id": 0,
                "patient_name": "$patient.full_name",
                "birthday": {"$dateToString": {"format": "%Y", "date": "$patient.date_of_birth"}},
                "gender": "$patient.gender",
                "address": "$patient.address",
                "doctor_name": "$doctor.full_name",
                "reason": {"$ifNull": ["$reason", "No"]},
                "date": {
                    "$ifNull": [
                        {"$dateToString": {"format": "%d-%m-%Y %H:%M", "date": "$appointment_date"}},
                        "None"
                    ]
                }
            }
        }
    ]
    
    appointments = list(db['appointments'].aggregate(pipeline))
    
    # Calculate column widths
    headers = ["No", "Patient name", "Birthday", "Gender", "Address", "Doctor name", "Reason", "Date"]
    widths = [len(h) for h in headers]
    
    # Find maximum width for each column
    for appt in appointments:
        widths[0] = max(widths[0], len(str(appointments.index(appt)+1)))
        widths[1] = max(widths[1], len(appt['patient_name']))
        widths[2] = max(widths[2], len(appt['birthday']))
        widths[3] = max(widths[3], len(appt['gender']))
        widths[4] = max(widths[4], len(appt['address']))
        widths[5] = max(widths[5], len(appt['doctor_name']))
        widths[6] = max(widths[6], len(appt['reason']))
        widths[7] = max(widths[7], len(appt['date']))
    
    # Create format string
    fmt = "|" + "|".join(f" {{:<{w}}} " for w in widths) + "|"
    
    print("\nAPPOINTMENT REPORT")
    print(fmt.format(*headers))
    print("|" + "+".join("-"*(w+2) for w in widths) + "|")
    
    for idx, appt in enumerate(appointments, 1):
        print(fmt.format(
            str(idx),
            appt['patient_name'],
            appt['birthday'],
            appt['gender'],
            appt['address'],
            appt['doctor_name'],
            appt['reason'],
            appt['date']
        ))

# Get today's appointments 

def get_today_appointments(db):  
    pipeline = [
        {
            "$lookup": {
                "from": "patients",
                "localField": "patient_id",
                "foreignField": "_id",
                "as": "patient"
            }
        },
        {
            "$lookup": {
                "from": "doctors",
                "localField": "doctor_id",
                "foreignField": "_id",
                "as": "doctor"
            }
        },
        {
            "$unwind": "$patient"
        },
        {
            "$unwind": "$doctor"
        },
        {
            "$project": {
                "_id": 0,
                "address": "$patient.address",
                "patient_name": "$patient.full_name",
                "birthday": {"$dateToString": {"format": "%Y", "date": "$patient.date_of_birth"}},
                "gender": {
                    "$switch": {
                        "branches": [
                            {"case": {"$eq": ["$patient.gender", "Male"]}, "then": "Male"},
                            {"case": {"$eq": ["$patient.gender", "male"]}, "then": "Male"},
                            {"case": {"$eq": ["$patient.gender", "M"]}, "then": "Male"},
                            {"case": {"$eq": ["$patient.gender", "Female"]}, "then": "Female"},
                            {"case": {"$eq": ["$patient.gender", "female"]}, "then": "Female"},
                            {"case": {"$eq": ["$patient.gender", "F"]}, "then": "Female"}
                        ],
                        "default": "Other"
                    }
                },
                "doctor_name": "$doctor.full_name",
                "status": "$status",
                "note": {"$ifNull": ["$note", ""]},
                "appointment_date": {
                    "$ifNull": [
                        {"$dateToString": {"format": "%d-%m-%Y %H:%M", "date": "$appointment_date"}},
                        "Not scheduled"
                    ]
                }
            }
        },
        {
            "$sort": {"appointment_date": 1}
        }
    ]

    appointments = list(db['appointments'].aggregate(pipeline))

    if not appointments:
        print("\nNo appointments found in the system!")
        return

    # Calculate column widths
    headers = ["Address", "No", "Patient", "Birth", "Gender", 
               "Doctor", "Status", "Note", "Appointment Date"]
    widths = [len(h) for h in headers]
    
    for appt in appointments:
        widths[0] = max(widths[0], len(appt['address']))
        widths[1] = max(widths[1], 2)
        widths[2] = max(widths[2], len(appt['patient_name']))
        widths[3] = max(widths[3], len(appt['birthday']))
        widths[4] = max(widths[4], len(appt['gender']))
        widths[5] = max(widths[5], len(appt['doctor_name']))
        widths[6] = max(widths[6], len(appt['status']))
        widths[7] = max(widths[7], len(appt['note']))
        widths[8] = max(widths[8], len(appt['appointment_date']))

    # Create format string
    fmt = "|" + "|".join(f" {{:<{w}}} " for w in widths) + "|"
    separator = "|" + "+".join("-"*(w+2) for w in widths) + "|"

    print("\nALL APPOINTMENTS")
    print(fmt.format(*headers))
    print(separator)

    for idx, appt in enumerate(appointments, 1):
        print(fmt.format(
            appt['address'],
            str(idx),
            appt['patient_name'],
            appt['birthday'],
            appt['gender'],
            appt['doctor_name'],
            appt['status'],
            appt['note'],
            appt['appointment_date']
        ))

# Main function
def main():
    db = connect_to_database()
    if db is None:
        print("Failed to connect to database. Exiting program.")
        return
    
    while True:
        print("\nMEDICAL SERVICE MANAGEMENT SYSTEM")
        print("1. Add patients (3 patients)")
        print("2. Add doctors (5 doctors)")
        print("3. Add appointments (3 appointments)")
        print("4. Generate report")
        print("5. View today's appointments")
        print("0. Exit")
        
        choice = input("Select function: ")
        
        if choice == '1':
            add_patients(db)
        elif choice == '2':
            add_doctors(db)
        elif choice == '3':
            add_appointments(db)
        elif choice == '4':
            generate_report(db)
        elif choice == '5':
            get_today_appointments(db)
        elif choice == '0':
            print("Exiting program")
            break
        else:
            print("Invalid selection, please try again")

if __name__ == "__main__":
    main()