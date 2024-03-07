import base64
import json
import os
from uuid import UUID
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

from database.models import Patient, Doctor, HealthRecord, Medication, Appointment, Prescription
from utils.session import *


class RequestHandler(BaseHTTPRequestHandler):
    def authenticate(self):
        # Get the username and password from environment variables
        expected_username = os.environ.get('API_USERNAME', 'admin')
        expected_password = os.environ.get('API_PASSWORD', 'password')

        # Get the provided credentials from the request headers
        auth_header = self.headers.get('Authorization')
        if auth_header:
            _, credentials = auth_header.split(' ', 1)
            username, password = base64.b64decode(credentials).decode('utf-8').split(':', 1)

            # Check if the provided credentials match the expected ones
            if username == expected_username and password == expected_password:
                return True

        # If authentication fails, send a 401 Unauthorized response
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm="Restricted"')
        self.end_headers()
        self.wfile.write("Unauthorized".encode())
        return False

    def set_and_send_headers(self, status=200, content_type='application/json'):
        self.send_response(status)
        self.send_header('Content-type', content_type)
        self.end_headers()

    def get_requested_data(self):
        content_length = int(self.headers['Content-Length'])
        request_data = self.rfile.read(content_length)
        return json.loads(request_data.decode())

    def do_GET(self):
        if not self.authenticate():
            return

        parsed_url = urlparse(self.path)
        path = parsed_url.path
        query_params = parse_qs(parsed_url.query)

        # Get all entities
        if path == '/patients':
            patients = get_all_entities(Patient, query_params)
            self.set_and_send_headers()
            self.wfile.write(json.dumps(patients).encode())

        elif path == '/doctors':
            doctors = get_all_entities(Doctor, query_params)
            self.set_and_send_headers()
            self.wfile.write(json.dumps(doctors).encode())

        elif path == '/health-records':
            health_records = get_all_entities(HealthRecord, query_params)
            self.set_and_send_headers()
            self.wfile.write(json.dumps(health_records).encode())

        elif path == '/medications':
            medications = get_all_entities(Medication, query_params)
            self.set_and_send_headers()
            self.wfile.write(json.dumps(medications).encode())

        elif path == '/appointments':
            appointments = get_all_entities(Appointment, query_params)
            self.set_and_send_headers()
            self.wfile.write(json.dumps(appointments).encode())

        elif path == '/prescriptions':
            prescriptions = get_all_entities(Prescription, query_params)
            self.set_and_send_headers()
            self.wfile.write(json.dumps(prescriptions).encode())

        # Get entities by foreign key
        elif path.startswith('/appointments/by-patient'):
            patient_uuid = UUID(path.split('/')[-1])
            appointments = get_all_entities(Appointment, {'patient_uuid': patient_uuid})
            if appointments:
                self.set_and_send_headers()
                self.wfile.write(json.dumps(appointments).encode())
            else:
                self.send_error(404, message="Appointment not found")

        elif path.startswith('/appointments/by-doctor'):
            doctor_uuid = UUID(path.split('/')[-1])
            appointments = get_all_entities(Appointment, {'doctor_uuid': doctor_uuid})
            if appointments:
                self.set_and_send_headers()
                self.wfile.write(json.dumps(appointments).encode())
            else:
                self.send_error(404, message="Appointment not found")

        elif path.startswith('/prescriptions/by-patient'):
            patient_uuid = UUID(path.split('/')[-1])
            prescriptions = get_all_entities(Prescription, {'patient_uuid': patient_uuid})
            if prescriptions:
                self.set_and_send_headers()
                self.wfile.write(json.dumps(prescriptions).encode())
            else:
                self.send_error(404, message="Prescription not found")

        elif path.startswith('/prescriptions/by-doctor'):
            doctor_uuid = UUID(path.split('/')[-1])
            prescriptions = get_all_entities(Prescription, {'doctor_uuid': doctor_uuid})
            if prescriptions:
                self.set_and_send_headers()
                self.wfile.write(json.dumps(prescriptions).encode())
            else:
                self.send_error(404, message="Prescription not found")

        elif path.startswith('/prescriptions/by-medication'):
            medication_uuid = UUID(path.split('/')[-1])
            prescriptions = get_all_entities(Prescription, {'medication_uuid': medication_uuid})
            if prescriptions:
                self.set_and_send_headers()
                self.wfile.write(json.dumps(prescriptions).encode())
            else:
                self.send_error(404, message="Prescription not found")

        # Get a specific entity by its UUID
        elif path.startswith('/patients'):
            patient_uuid = UUID(path.split('/')[-1])
            patient = get_entity_by_uuid(Patient, patient_uuid)
            if patient:
                self.set_and_send_headers()
                self.wfile.write(json.dumps(patient).encode())
            else:
                self.send_error(404, message="Patient not found")

        elif path.startswith('/doctors'):
            doctor_uuid = UUID(path.split('/')[-1])
            doctor = get_entity_by_uuid(Doctor, doctor_uuid)
            if doctor:
                self.set_and_send_headers()
                self.wfile.write(json.dumps(doctor).encode())
            else:
                self.send_error(404, message="Doctor not found")

        elif path.startswith('/health-records'):
            health_record_uuid = UUID(path.split('/')[-1])
            health_record = get_entity_by_uuid(HealthRecord, health_record_uuid)
            if health_record:
                self.set_and_send_headers()
                self.wfile.write(json.dumps(health_record).encode())
            else:
                self.send_error(404, message="Health record not found")

        elif path.startswith('/medications/'):
            medication_uuid = UUID(path.split('/')[-1])
            medication = get_entity_by_uuid(Medication, medication_uuid)
            if medication:
                self.set_and_send_headers()
                self.wfile.write(json.dumps(medication).encode())
            else:
                self.send_error(404, message="Medication not found")

        elif path.startswith('/appointments'):
            appointment_uuid = UUID(path.split('/')[-1])
            appointment = get_entity_by_uuid(Appointment, appointment_uuid)
            if appointment:
                self.set_and_send_headers()
                self.wfile.write(json.dumps(appointment).encode())
            else:
                self.send_error(404, message="Appointment not found")

        elif path.startswith('/prescriptions'):
            prescription_uuid = UUID(path.split('/')[-1])
            prescription = get_entity_by_uuid(Prescription, prescription_uuid)
            if prescription:
                self.set_and_send_headers()
                self.wfile.write(json.dumps(prescription).encode())
            else:
                self.send_error(404, message="Prescription not found")

        else:
            self.send_error(404, message="Page not found")

    def do_POST(self):
        if not self.authenticate():
            return

        parsed_url = urlparse(self.path)
        path = parsed_url.path

        if path == '/patients':
            new_patient_data = self.get_requested_data()
            create_entity(Patient, new_patient_data)
            self.set_and_send_headers(201, 'text/plain')
            self.wfile.write("New patient created".encode())

        elif path == '/doctors':
            new_doctor_data = self.get_requested_data()
            create_entity(Doctor, new_doctor_data)
            self.set_and_send_headers(201, 'text/plain')
            self.wfile.write("New doctor created".encode())

        elif path == '/health-records':
            new_health_record_data = self.get_requested_data()
            create_entity(HealthRecord, new_health_record_data)
            self.set_and_send_headers(201, 'text/plain')
            self.wfile.write("New health record created".encode())

        elif path == '/medications':
            new_medication_data = self.get_requested_data()
            create_entity(Medication, new_medication_data)
            self.set_and_send_headers(201, 'text/plain')
            self.wfile.write("New medication created".encode())

        elif path == '/appointments':
            new_appointment_data = self.get_requested_data()
            create_entity(Appointment, new_appointment_data)
            self.set_and_send_headers(201, 'text/plain')
            self.wfile.write("New appointment created".encode())

        elif path == '/prescriptions':
            new_prescription_data = self.get_requested_data()
            create_entity(Prescription, new_prescription_data)
            self.set_and_send_headers(201, 'text/plain')
            self.wfile.write("New prescription created".encode())

        else:
            self.send_error(404, message="Page not found")

    def do_PUT(self):
        if not self.authenticate():
            return

        parsed_url = urlparse(self.path)
        path = parsed_url.path

        if path.startswith('/patients'):
            patient_uuid = UUID(path.split('/')[-1])
            updated_patient_data = self.get_requested_data()
            updated_patient = update_entity(Patient, patient_uuid, updated_patient_data)
            if updated_patient:
                self.set_and_send_headers(200, 'text/plain')
                self.wfile.write("Patient updated".encode())
            else:
                self.send_error(500)

        elif path.startswith('/doctors'):
            doctor_uuid = UUID(path.split('/')[-1])
            updated_doctor_data = self.get_requested_data()
            updated_doctor = update_entity(Doctor, doctor_uuid, updated_doctor_data)
            if updated_doctor:
                self.set_and_send_headers(200, 'text/plain')
                self.wfile.write("Doctor updated".encode())
            else:
                self.send_error(500)

        elif path.startswith('/health-records'):
            health_record_uuid = UUID(path.split('/')[-1])
            updated_health_record_data = self.get_requested_data()
            updated_health_record = update_entity(HealthRecord, health_record_uuid, updated_health_record_data)
            if updated_health_record:
                self.set_and_send_headers(200, 'text/plain')
                self.wfile.write("Health record updated".encode())
            else:
                self.send_error(500)

        elif path.startswith('/medications'):
            medication_uuid = UUID(path.split('/')[-1])
            updated_medication_data = self.get_requested_data()
            updated_medication = update_entity(Medication, medication_uuid, updated_medication_data)
            if updated_medication:
                self.set_and_send_headers(200, 'text/plain')
                self.wfile.write("Medication updated".encode())
            else:
                self.send_error(500)

        elif path.startswith('/appointments'):
            appointment_uuid = UUID(path.split('/')[-1])
            updated_appointment_data = self.get_requested_data()
            updated_appointment = update_entity(Appointment, appointment_uuid, updated_appointment_data)
            if updated_appointment:
                self.set_and_send_headers(200, 'text/plain')
                self.wfile.write("Appointment updated".encode())
            else:
                self.send_error(500)

        elif path.startswith('/prescriptions'):
            prescription_uuid = UUID(path.split('/')[-1])
            updated_prescription_data = self.get_requested_data()
            updated_prescription = update_entity(Prescription, prescription_uuid, updated_prescription_data)
            if updated_prescription:
                self.set_and_send_headers(200, 'text/plain')
                self.wfile.write("Prescription updated".encode())
            else:
                self.send_error(500)

        else:
            self.send_error(404, message="Page not found")

    def do_DELETE(self):
        if not self.authenticate():
            return

        parsed_url = urlparse(self.path)
        path = parsed_url.path

        if path.startswith('/patients'):
            patient_uuid = UUID(path.split('/')[-1])
            deleted_patient = delete_entity(Patient, patient_uuid)
            if deleted_patient:
                self.set_and_send_headers(200, 'text/plain')
                self.wfile.write("Patient deleted".encode())
            else:
                self.send_error(404, message="Patient not found")

        elif path.startswith('/doctors'):
            doctor_uuid = UUID(path.split('/')[-1])
            deleted_doctor = delete_entity(Doctor, doctor_uuid)
            if deleted_doctor:
                self.set_and_send_headers(200, 'text/plain')
                self.wfile.write("Doctor deleted".encode())
            else:
                self.send_error(404, message="Doctor not found")

        elif path.startswith('/health-records'):
            health_record_uuid = UUID(path.split('/')[-1])
            deleted_health_record = delete_entity(HealthRecord, health_record_uuid)
            if deleted_health_record:
                self.set_and_send_headers(200, 'text/plain')
                self.wfile.write("Health record deleted".encode())
            else:
                self.send_error(404, message="Health record not found")

        elif path.startswith('/medications'):
            medication_uuid = UUID(path.split('/')[-1])
            deleted_medication = delete_entity(Medication, medication_uuid)
            if deleted_medication:
                self.set_and_send_headers(200, 'text/plain')
                self.wfile.write("Medication deleted".encode())
            else:
                self.send_error(404, message="Medication not found")

        elif path.startswith('/appointments'):
            appointment_uuid = UUID(path.split('/')[-1])
            deleted_appointment = delete_entity(Appointment, appointment_uuid)
            if deleted_appointment:
                self.set_and_send_headers(200, 'text/plain')
                self.wfile.write("Appointment deleted".encode())
            else:
                self.send_error(404, message="Appointment not found")

        elif path.startswith('/prescriptions'):
            prescription_uuid = UUID(path.split('/')[-1])
            deleted_prescription = delete_entity(Prescription, prescription_uuid)
            if deleted_prescription:
                self.set_and_send_headers(200, 'text/plain')
                self.wfile.write("Prescription deleted".encode())
            else:
                self.send_error(404, message="Prescription not found")

        else:
            self.send_error(404, message="Page not found")
