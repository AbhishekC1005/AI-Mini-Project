"""Simplified Hospital data query tool for CSV analysis."""
import pandas as pd
import os
from typing import Optional
from math import radians, sin, cos, sqrt, atan2


class HospitalDataTool:
    """Tool for querying hospital data from CSV."""
    
    def __init__(self, csv_path="agent/data/hospital_trends.csv"):
        """Initialize with CSV file path."""
        self.csv_path = csv_path
        self.df = None
        if os.path.exists(csv_path):
            self._load_data()
            self._add_location_column()
    
    def _load_data(self):
        """Load CSV data into pandas DataFrame."""
        if os.path.exists(self.csv_path):
            self.df = pd.read_csv(self.csv_path)
        else:
            self.df = None
    
    def _add_location_column(self):
        """Add location column to CSV if it doesn't exist."""
        if self.df is None:
            return
        
        if 'location' not in self.df.columns:
            # Define locations for each hospital
            location_mapping = {
                'H001': 'New York, NY',
                'H002': 'Los Angeles, CA',
                'H003': 'Chicago, IL',
                'H004': 'Houston, TX',
                'H005': 'Phoenix, AZ'
            }
            
            # Add location column
            self.df['location'] = self.df['hospital_id'].map(location_mapping)
            
            # Save updated CSV
            self.df.to_csv(self.csv_path, index=False)
            print(f"✓ Added location column to {self.csv_path}")
    
    def get_hospital_count(self) -> int:
        """Get total number of unique hospitals."""
        if self.df is None:
            return 0
        return self.df['hospital_id'].nunique()
    
    def get_hospital_names(self) -> list:
        """Get list of all hospital names with IDs and locations."""
        if self.df is None:
            return []
        hospitals = self.df[['hospital_id', 'hospital_name', 'location']].drop_duplicates()
        return hospitals.to_dict('records')
    
    def get_hospital_details_by_date(self, hospital_name: str, date: str) -> dict:
        """
        Get details of a specific hospital for a specific date.
        
        Args:
            hospital_name: Name of the hospital
            date: Date in format 'YYYY-MM-DD'
            
        Returns:
            dict: Hospital details for that date
        """
        # Filter by hospital name and date
        hospital_data = self.df[
            (self.df['hospital_name'] == hospital_name) & 
            (self.df['date'] == date)
        ]
        
        if hospital_data.empty:
            return {"error": f"No data found for hospital '{hospital_name}' on date '{date}'"}
        
        # Convert to dictionary
        return hospital_data.iloc[0].to_dict()
    
    def get_column_value(self, hospital_name: str, column_name: str, date: Optional[str] = None) -> dict:
        """
        Get specific column value for a hospital.
        
        Args:
            hospital_name: Name of the hospital
            column_name: Name of the column to retrieve
            date: Optional date (if not provided, returns latest)
            
        Returns:
            dict: Column value(s)
        """
        # Check if column exists
        if column_name not in self.df.columns:
            return {"error": f"Column '{column_name}' not found. Use get_column_names() to see available columns."}
        
        # Filter by hospital name
        hospital_data = self.df[self.df['hospital_name'] == hospital_name]
        
        if hospital_data.empty:
            return {"error": f"Hospital '{hospital_name}' not found"}
        
        # Filter by date if provided
        if date:
            hospital_data = hospital_data[hospital_data['date'] == date]
            if hospital_data.empty:
                return {"error": f"No data found for hospital '{hospital_name}' on date '{date}'"}
            
            return {
                "hospital_name": hospital_name,
                "column": column_name,
                "date": date,
                "value": hospital_data.iloc[0][column_name]
            }
        else:
            # Return all dates
            values = hospital_data[['date', column_name]].to_dict('records')
            return {
                "hospital_name": hospital_name,
                "column": column_name,
                "values": values
            }
    
    def get_column_names(self) -> list:
        """Get all column names available in the CSV."""
        return list(self.df.columns)
    
    def get_hospital_location(self, hospital_name: str) -> dict:
        """
        Get location of a specific hospital.
        
        Args:
            hospital_name: Name of the hospital
            
        Returns:
            dict: Hospital location information with coordinates
        """
        hospital_data = self.df[self.df['hospital_name'] == hospital_name]
        
        if hospital_data.empty:
            return {"error": f"Hospital '{hospital_name}' not found"}
        
        row = hospital_data.iloc[0]
        
        # Parse coordinates from location column (format: "lat,lon")
        coords = row['location'].split(',')
        latitude = float(coords[0])
        longitude = float(coords[1])
        
        return {
            "hospital_name": hospital_name,
            "hospital_id": row['hospital_id'],
            "location": row['location'],
            "region": row['region'],
            "latitude": latitude,
            "longitude": longitude
        }
    
    def calculate_distance(self, hospital_name1: str, hospital_name2: str) -> dict:
        """
        Calculate distance between two hospitals using Haversine formula.
        
        Args:
            hospital_name1: Name of first hospital
            hospital_name2: Name of second hospital
            
        Returns:
            dict: Distance information in kilometers
        """
        # Get coordinates for both hospitals
        hosp1_data = self.df[self.df['hospital_name'] == hospital_name1]
        hosp2_data = self.df[self.df['hospital_name'] == hospital_name2]
        
        if hosp1_data.empty:
            return {"error": f"Hospital '{hospital_name1}' not found"}
        if hosp2_data.empty:
            return {"error": f"Hospital '{hospital_name2}' not found"}
        
        # Parse coordinates from location column (format: "lat,lon")
        coords1 = hosp1_data.iloc[0]['location'].split(',')
        lat1 = float(coords1[0])
        lon1 = float(coords1[1])
        
        coords2 = hosp2_data.iloc[0]['location'].split(',')
        lat2 = float(coords2[0])
        lon2 = float(coords2[1])
        
        # Haversine formula
        R = 6371  # Earth's radius in kilometers
        
        lat1_rad = radians(lat1)
        lat2_rad = radians(lat2)
        delta_lat = radians(lat2 - lat1)
        delta_lon = radians(lon2 - lon1)
        
        a = sin(delta_lat / 2) ** 2 + cos(lat1_rad) * cos(lat2_rad) * sin(delta_lon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance_km = R * c
        
        return {
            "from_hospital": hospital_name1,
            "to_hospital": hospital_name2,
            "distance_km": round(distance_km, 2),
            "from_coordinates": {"latitude": lat1, "longitude": lon1},
            "to_coordinates": {"latitude": lat2, "longitude": lon2}
        }
    
    def get_all_distances(self) -> dict:
        """
        Calculate distances between all pairs of hospitals.
        
        Returns:
            dict: Distance matrix for all hospitals
        """
        hospitals = self.df[['hospital_id', 'hospital_name']].drop_duplicates()
        distances = []
        
        for i, hosp1 in hospitals.iterrows():
            for j, hosp2 in hospitals.iterrows():
                if hosp1['hospital_id'] < hosp2['hospital_id']:  # Avoid duplicates
                    dist_info = self.calculate_distance(hosp1['hospital_name'], hosp2['hospital_name'])
                    if "error" not in dist_info:
                        distances.append(dist_info)
        
        return {
            "total_pairs": len(distances),
            "distances": distances
        }
    
    def get_date_range(self) -> dict:
        """Get the date range of available data."""
        dates = sorted(self.df['date'].unique())
        return {
            "start_date": dates[0],
            "end_date": dates[-1],
            "total_days": len(dates),
            "all_dates": dates
        }


# Initialize global instance
hospital_tool = HospitalDataTool()


# ============================================================================
# Department, Doctor, and Patient Data Tools
# ============================================================================

class DepartmentDataTool:
    """Tool for querying department data."""
    
    def __init__(self, csv_path="agent/data/department.csv"):
        self.csv_path = csv_path
        self.df = pd.read_csv(csv_path) if os.path.exists(csv_path) else None
    
    def get_all_departments(self) -> list:
        """Get list of all departments."""
        if self.df is None:
            return []
        return self.df.to_dict('records')
    
    def get_department_by_name(self, department_name: str) -> dict:
        """Get department details by name."""
        if self.df is None:
            return {"error": "Department data not found"}
        
        dept = self.df[self.df['department_name'].str.contains(department_name, case=False, na=False)]
        if dept.empty:
            return {"error": f"Department '{department_name}' not found"}
        return dept.iloc[0].to_dict()
    
    def get_departments_by_floor(self, floor: str) -> list:
        """Get all departments on a specific floor."""
        if self.df is None:
            return []
        
        depts = self.df[self.df['floor'].str.contains(floor, case=False, na=False)]
        return depts.to_dict('records')
    
    def get_departments_by_building(self, building: str) -> list:
        """Get all departments in a specific building."""
        if self.df is None:
            return []
        
        depts = self.df[self.df['building'].str.contains(building, case=False, na=False)]
        return depts.to_dict('records')


class DoctorDataTool:
    """Tool for querying doctor data."""
    
    def __init__(self, csv_path="agent/data/doctor.csv"):
        self.csv_path = csv_path
        self.df = pd.read_csv(csv_path) if os.path.exists(csv_path) else None
    
    def get_all_doctors(self) -> list:
        """Get list of all doctors."""
        if self.df is None:
            return []
        return self.df.to_dict('records')
    
    def get_doctor_by_name(self, doctor_name: str) -> dict:
        """Get doctor details by name."""
        if self.df is None:
            return {"error": "Doctor data not found"}
        
        doctor = self.df[self.df['doctor_name'].str.contains(doctor_name, case=False, na=False)]
        if doctor.empty:
            return {"error": f"Doctor '{doctor_name}' not found"}
        return doctor.iloc[0].to_dict()
    
    def get_doctors_by_specialization(self, specialization: str) -> list:
        """Get all doctors with a specific specialization."""
        if self.df is None:
            return []
        
        doctors = self.df[self.df['specialization'].str.contains(specialization, case=False, na=False)]
        return doctors.to_dict('records')
    
    def get_doctors_by_department(self, department_id: str) -> list:
        """Get all doctors in a specific department."""
        if self.df is None:
            return []
        
        doctors = self.df[self.df['department_id'] == department_id]
        return doctors.to_dict('records')
    
    def get_available_doctors(self, day: str) -> list:
        """Get doctors available on a specific day."""
        if self.df is None:
            return []
        
        doctors = self.df[self.df['available_days'].str.contains(day, case=False, na=False)]
        return doctors.to_dict('records')


class PatientDataTool:
    """Tool for querying patient data."""
    
    def __init__(self, csv_path="agent/data/patient.csv"):
        self.csv_path = csv_path
        self.df = pd.read_csv(csv_path) if os.path.exists(csv_path) else None
    
    def get_all_patients(self) -> list:
        """Get list of all patients."""
        if self.df is None:
            return []
        return self.df.to_dict('records')
    
    def get_patient_by_name(self, patient_name: str) -> dict:
        """Get patient details by name."""
        if self.df is None:
            return {"error": "Patient data not found"}
        
        patient = self.df[self.df['patient_name'].str.contains(patient_name, case=False, na=False)]
        if patient.empty:
            return {"error": f"Patient '{patient_name}' not found"}
        return patient.iloc[0].to_dict()
    
    def get_patient_by_room(self, room_number: str) -> dict:
        """Get patient details by room number."""
        if self.df is None:
            return {"error": "Patient data not found"}
        
        patient = self.df[self.df['room_number'] == room_number]
        if patient.empty:
            return {"error": f"No patient found in room '{room_number}'"}
        return patient.iloc[0].to_dict()
    
    def get_patients_by_disease(self, disease: str) -> list:
        """Get all patients with a specific disease."""
        if self.df is None:
            return []
        
        patients = self.df[self.df['disease'].str.contains(disease, case=False, na=False)]
        return patients.to_dict('records')
    
    def get_patients_by_doctor(self, doctor_id: str) -> list:
        """Get all patients under a specific doctor."""
        if self.df is None:
            return []
        
        patients = self.df[self.df['attending_doctor_id'] == doctor_id]
        return patients.to_dict('records')
    
    def get_patients_by_floor(self, floor: str) -> list:
        """Get all patients on a specific floor."""
        if self.df is None:
            return []
        
        patients = self.df[self.df['floor'].str.contains(floor, case=False, na=False)]
        return patients.to_dict('records')
    
    def get_direction_to_patient(self, patient_name: str) -> dict:
        """Get directions to a patient's room."""
        if self.df is None:
            return {"error": "Patient data not found"}
        
        patient = self.df[self.df['patient_name'].str.contains(patient_name, case=False, na=False)]
        if patient.empty:
            return {"error": f"Patient '{patient_name}' not found"}
        
        p = patient.iloc[0]
        return {
            "patient_name": p['patient_name'],
            "room_number": p['room_number'],
            "floor": p['floor'],
            "building": p['building'],
            "directions": p['direction_to_room']
        }


# Initialize global instances
department_tool = DepartmentDataTool()
doctor_tool = DoctorDataTool()
patient_tool = PatientDataTool()
