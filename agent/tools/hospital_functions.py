"""Simplified hospital data query functions for ADK agent."""
from typing import Optional
from agent.tools.hospital_data import hospital_tool


def get_hospital_count() -> str:
    """
    Get the total number of hospitals in the system.
    
    Returns:
        str: Number of hospitals
    """
    try:
        count = hospital_tool.get_hospital_count()
        return f"There are {count} hospitals in the system."
    except Exception as e:
        return f"Error: {str(e)}"


def get_hospital_names() -> str:
    """
    Get the names, IDs, and locations of all hospitals.
    
    Returns:
        str: List of hospital names with IDs and locations
    """
    try:
        hospitals = hospital_tool.get_hospital_names()
        result = "Hospitals in the system:\n\n"
        for hosp in hospitals:
            result += f"• {hosp['hospital_name']} (ID: {hosp['hospital_id']})\n"
            result += f"  Location: {hosp['location']}\n\n"
        return result
    except Exception as e:
        return f"Error: {str(e)}"


def get_hospital_details_by_date(hospital_name: str, date: str) -> str:
    """
    Get detailed information for a specific hospital on a specific date.
    
    Args:
        hospital_name: The hospital name (e.g., 'City General Hospital')
        date: Date in format 'YYYY-MM-DD' (e.g., '2024-10-20')
        
    Returns:
        str: Detailed hospital information for that date
    """
    try:
        info = hospital_tool.get_hospital_details_by_date(hospital_name, date)
        
        if "error" in info:
            return info["error"]
        
        # Format the output
        result = f"📊 Hospital Details for {hospital_name} on {date}\n\n"
        result += f"Hospital ID: {info['hospital_id']}\n"
        result += f"Location: {info['location']}\n"
        result += f"Region: {info['region']}\n\n"
        
        result += f"🛏️ Beds:\n"
        result += f"  • Capacity: {info['bed_capacity']}\n"
        result += f"  • Occupied: {info['beds_occupied']}\n"
        result += f"  • Available: {info['beds_available']}\n\n"
        
        result += f"🏥 ICU:\n"
        result += f"  • Total: {info['icu_beds_total']}\n"
        result += f"  • Occupied: {info['icu_beds_occupied']}\n\n"
        
        result += f"🫁 Ventilators:\n"
        result += f"  • Total: {info['ventilators_total']}\n"
        result += f"  • In Use: {info['ventilators_in_use']}\n"
        result += f"  • Available: {info['ventilators_available']}\n\n"
        
        result += f"👨‍⚕️ Staff:\n"
        result += f"  • Doctors: {info['doctors_available']}/{info['doctors_total']} available\n"
        result += f"  • Nurses: {info['nurses_available']}/{info['nurses_total']} available\n"
        result += f"  • Paramedics: {info['paramedics_available']}/{info['paramedics_total']} available\n\n"
        
        result += f"📈 Patient Activity:\n"
        result += f"  • Admissions: {info['patient_admissions']}\n"
        result += f"  • Discharges: {info['patient_discharges']}\n"
        result += f"  • Emergency Visits: {info['emergency_visits']}\n"
        result += f"  • Surgeries: {info['surgery_count']}\n\n"
        
        result += f"🦠 Infectious Cases:\n"
        result += f"  • COVID: {info['covid_cases']}\n"
        result += f"  • Flu: {info['flu_cases']}\n"
        result += f"  • Other: {info['other_infectious_cases']}\n\n"
        
        result += f"⚠️ Burnout Risk: {info['burnout_risk_score']}\n"
        result += f"⭐ Patient Satisfaction: {info['avg_patient_satisfaction']}/5.0\n"
        
        return result
    except Exception as e:
        return f"Error: {str(e)}"


def get_column_value(hospital_name: str, column_name: str, date: Optional[str] = None) -> str:
    """
    Get a specific column value for a hospital.
    
    Args:
        hospital_name: The hospital name
        column_name: The column name to retrieve
        date: Optional date (if not provided, returns all dates)
        
    Returns:
        str: Column value(s)
    """
    try:
        result = hospital_tool.get_column_value(hospital_name, column_name, date)
        
        if "error" in result:
            return result["error"]
        
        if date:
            return f"{column_name} for {hospital_name} on {date}: {result['value']}"
        else:
            output = f"{column_name} for {hospital_name} across all dates:\n\n"
            for item in result['values']:
                output += f"  • {item['date']}: {item[column_name]}\n"
            return output
    except Exception as e:
        return f"Error: {str(e)}"


def get_column_names() -> str:
    """
    Get all available column names in the hospital data CSV.
    
    Returns:
        str: List of column names
    """
    try:
        columns = hospital_tool.get_column_names()
        result = "Available columns in hospital data:\n\n"
        for i, col in enumerate(columns, 1):
            result += f"{i}. {col}\n"
        return result
    except Exception as e:
        return f"Error: {str(e)}"


def get_hospital_location(hospital_name: str) -> str:
    """
    Get the location of a specific hospital.
    
    Args:
        hospital_name: The hospital name
        
    Returns:
        str: Hospital location information
    """
    try:
        info = hospital_tool.get_hospital_location(hospital_name)
        
        if "error" in info:
            return info["error"]
        
        result = f"📍 Location Information\n\n"
        result += f"Hospital: {info['hospital_name']}\n"
        result += f"ID: {info['hospital_id']}\n"
        result += f"Location: {info['location']}\n"
        result += f"Region: {info['region']}\n"
        
        return result
    except Exception as e:
        return f"Error: {str(e)}"


def get_data_date_range() -> str:
    """
    Get the date range of available hospital data.
    
    Returns:
        str: Date range information
    """
    try:
        info = hospital_tool.get_date_range()
        result = f"📅 Available Data Range\n\n"
        result += f"Start Date: {info['start_date']}\n"
        result += f"End Date: {info['end_date']}\n"
        result += f"Total Days: {info['total_days']}\n\n"
        result += f"All Dates:\n"
        for date in info['all_dates']:
            result += f"  • {date}\n"
        return result
    except Exception as e:
        return f"Error: {str(e)}"


def calculate_distance_between_hospitals(hospital_name1: str, hospital_name2: str) -> str:
    """
    Calculate the distance between two hospitals.
    
    Args:
        hospital_name1: Name of the first hospital
        hospital_name2: Name of the second hospital
        
    Returns:
        str: Distance information
    """
    try:
        info = hospital_tool.calculate_distance(hospital_name1, hospital_name2)
        
        if "error" in info:
            return info["error"]
        
        result = f"📏 Distance Calculation\n\n"
        result += f"From: {info['from_hospital']}\n"
        result += f"  Coordinates: ({info['from_coordinates']['latitude']}, {info['from_coordinates']['longitude']})\n\n"
        result += f"To: {info['to_hospital']}\n"
        result += f"  Coordinates: ({info['to_coordinates']['latitude']}, {info['to_coordinates']['longitude']})\n\n"
        result += f"Distance: {info['distance_km']} km\n"
        
        return result
    except Exception as e:
        return f"Error: {str(e)}"


def get_all_hospital_distances() -> str:
    """
    Get distances between all pairs of hospitals.
    
    Returns:
        str: Distance matrix for all hospitals
    """
    try:
        info = hospital_tool.get_all_distances()
        
        result = f"📏 Hospital Distance Matrix\n\n"
        result += f"Total Hospital Pairs: {info['total_pairs']}\n\n"
        
        for dist in info['distances']:
            result += f"• {dist['from_hospital']} ↔ {dist['to_hospital']}: {dist['distance_km']} km\n"
        
        return result
    except Exception as e:
        return f"Error: {str(e)}"



# ============================================================================
# Department Functions
# ============================================================================

def get_all_departments() -> str:
    """
    Get list of all hospital departments.
    
    Returns:
        str: List of all departments with locations
    """
    try:
        from agent.tools.hospital_data import department_tool
        departments = department_tool.get_all_departments()
        
        if not departments:
            return "No department data available."
        
        result = "🏥 Hospital Departments:\n\n"
        for dept in departments:
            result += f"• {dept['department_name']}\n"
            result += f"  Location: {dept['floor']}, {dept['building']}\n"
            result += f"  Extension: {dept['contact_extension']}\n\n"
        
        return result
    except Exception as e:
        return f"Error: {str(e)}"


def find_department(department_name: str) -> str:
    """
    Find a specific department by name.
    
    Args:
        department_name: Name of the department
        
    Returns:
        str: Department details and location
    """
    try:
        from agent.tools.hospital_data import department_tool
        dept = department_tool.get_department_by_name(department_name)
        
        if "error" in dept:
            return dept["error"]
        
        result = f"📍 {dept['department_name']}\n\n"
        result += f"Location: {dept['floor']}, {dept['building']}\n"
        result += f"Contact Extension: {dept['contact_extension']}\n"
        
        return result
    except Exception as e:
        return f"Error: {str(e)}"


def get_departments_on_floor(floor: str) -> str:
    """
    Get all departments on a specific floor.
    
    Args:
        floor: Floor name (e.g., "First Floor", "Ground Floor")
        
    Returns:
        str: List of departments on that floor
    """
    try:
        from agent.tools.hospital_data import department_tool
        departments = department_tool.get_departments_by_floor(floor)
        
        if not departments:
            return f"No departments found on {floor}."
        
        result = f"Departments on {floor}:\n\n"
        for dept in departments:
            result += f"• {dept['department_name']} - {dept['building']}\n"
        
        return result
    except Exception as e:
        return f"Error: {str(e)}"


# ============================================================================
# Doctor Functions
# ============================================================================

def get_all_doctors() -> str:
    """
    Get list of all doctors.
    
    Returns:
        str: List of all doctors with specializations
    """
    try:
        from agent.tools.hospital_data import doctor_tool
        doctors = doctor_tool.get_all_doctors()
        
        if not doctors:
            return "No doctor data available."
        
        result = "👨‍⚕️ Hospital Doctors:\n\n"
        for doc in doctors:
            result += f"• {doc['doctor_name']} - {doc['specialization']}\n"
            result += f"  Available: {doc['available_days']}, {doc['available_time_start']}-{doc['available_time_end']}\n\n"
        
        return result
    except Exception as e:
        return f"Error: {str(e)}"


def find_doctor(doctor_name: str) -> str:
    """
    Find a specific doctor by name.
    
    Args:
        doctor_name: Name of the doctor
        
    Returns:
        str: Doctor details and availability
    """
    try:
        from agent.tools.hospital_data import doctor_tool
        doctor = doctor_tool.get_doctor_by_name(doctor_name)
        
        if "error" in doctor:
            return doctor["error"]
        
        result = f"👨‍⚕️ {doctor['doctor_name']}\n\n"
        result += f"Specialization: {doctor['specialization']}\n"
        result += f"Experience: {doctor['years_experience']} years\n"
        result += f"Available: {doctor['available_days']}\n"
        result += f"Time: {doctor['available_time_start']} - {doctor['available_time_end']}\n"
        result += f"Contact: {doctor['contact_number']}\n"
        
        return result
    except Exception as e:
        return f"Error: {str(e)}"


def find_doctors_by_specialization(specialization: str) -> str:
    """
    Find doctors by specialization.
    
    Args:
        specialization: Medical specialization (e.g., "Cardiologist", "Pediatrician")
        
    Returns:
        str: List of doctors with that specialization
    """
    try:
        from agent.tools.hospital_data import doctor_tool
        doctors = doctor_tool.get_doctors_by_specialization(specialization)
        
        if not doctors:
            return f"No doctors found with specialization: {specialization}"
        
        result = f"Doctors specializing in {specialization}:\n\n"
        for doc in doctors:
            result += f"• {doc['doctor_name']}\n"
            result += f"  Available: {doc['available_days']}, {doc['available_time_start']}-{doc['available_time_end']}\n\n"
        
        return result
    except Exception as e:
        return f"Error: {str(e)}"


def get_available_doctors_today(day: str) -> str:
    """
    Get doctors available on a specific day.
    
    Args:
        day: Day of the week (e.g., "Monday", "Tuesday")
        
    Returns:
        str: List of available doctors
    """
    try:
        from agent.tools.hospital_data import doctor_tool
        doctors = doctor_tool.get_available_doctors(day)
        
        if not doctors:
            return f"No doctors available on {day}."
        
        result = f"Doctors available on {day}:\n\n"
        for doc in doctors:
            result += f"• {doc['doctor_name']} - {doc['specialization']}\n"
            result += f"  Time: {doc['available_time_start']}-{doc['available_time_end']}\n\n"
        
        return result
    except Exception as e:
        return f"Error: {str(e)}"


# ============================================================================
# Patient Functions
# ============================================================================

def get_all_patients() -> str:
    """
    Get list of all current patients.
    
    Returns:
        str: List of all patients
    """
    try:
        from agent.tools.hospital_data import patient_tool
        patients = patient_tool.get_all_patients()
        
        if not patients:
            return "No patient data available."
        
        result = "🏥 Current Patients:\n\n"
        for patient in patients:
            result += f"• {patient['patient_name']} - Room {patient['room_number']}\n"
            result += f"  Condition: {patient['disease']}\n\n"
        
        return result
    except Exception as e:
        return f"Error: {str(e)}"


def find_patient(patient_name: str) -> str:
    """
    Find a specific patient by name.
    
    Args:
        patient_name: Name of the patient
        
    Returns:
        str: Patient details and room location
    """
    try:
        from agent.tools.hospital_data import patient_tool
        patient = patient_tool.get_patient_by_name(patient_name)
        
        if "error" in patient:
            return patient["error"]
        
        result = f"👤 {patient['patient_name']}\n\n"
        result += f"Age: {patient['age']}, Gender: {patient['gender']}\n"
        result += f"Room: {patient['room_number']}\n"
        result += f"Location: {patient['floor']}, {patient['building']}\n"
        result += f"Condition: {patient['disease']}\n"
        result += f"Admitted: {patient['admitted_date']}\n"
        result += f"Relative: {patient['relative_name']} ({patient['relative_contact']})\n"
        
        return result
    except Exception as e:
        return f"Error: {str(e)}"


def find_patient_by_room(room_number: str) -> str:
    """
    Find patient by room number.
    
    Args:
        room_number: Room number (e.g., "301", "ICU-05")
        
    Returns:
        str: Patient details
    """
    try:
        from agent.tools.hospital_data import patient_tool
        patient = patient_tool.get_patient_by_room(room_number)
        
        if "error" in patient:
            return patient["error"]
        
        result = f"Room {room_number}:\n\n"
        result += f"Patient: {patient['patient_name']}\n"
        result += f"Age: {patient['age']}, Gender: {patient['gender']}\n"
        result += f"Condition: {patient['disease']}\n"
        result += f"Relative: {patient['relative_name']} ({patient['relative_contact']})\n"
        
        return result
    except Exception as e:
        return f"Error: {str(e)}"


def get_directions_to_patient(patient_name: str) -> str:
    """
    Get directions to a patient's room.
    
    Args:
        patient_name: Name of the patient
        
    Returns:
        str: Detailed directions to the patient's room
    """
    try:
        from agent.tools.hospital_data import patient_tool
        directions = patient_tool.get_direction_to_patient(patient_name)
        
        if "error" in directions:
            return directions["error"]
        
        result = f"🗺️ Directions to {directions['patient_name']}\n\n"
        result += f"Room: {directions['room_number']}\n"
        result += f"Location: {directions['floor']}, {directions['building']}\n\n"
        result += f"Directions:\n{directions['directions']}\n"
        
        return result
    except Exception as e:
        return f"Error: {str(e)}"


def find_patients_by_disease(disease: str) -> str:
    """
    Find patients with a specific disease.
    
    Args:
        disease: Disease name
        
    Returns:
        str: List of patients with that disease
    """
    try:
        from agent.tools.hospital_data import patient_tool
        patients = patient_tool.get_patients_by_disease(disease)
        
        if not patients:
            return f"No patients found with disease: {disease}"
        
        result = f"Patients with {disease}:\n\n"
        for patient in patients:
            result += f"• {patient['patient_name']} - Room {patient['room_number']}\n"
        
        return result
    except Exception as e:
        return f"Error: {str(e)}"
