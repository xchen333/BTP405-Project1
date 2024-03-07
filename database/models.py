import uuid

from sqlalchemy import create_engine, Column, Integer, String, Date, Text, ForeignKey, UUID
from sqlalchemy.ext.declarative import declarative_base

# Define your database connection string
DATABASE_URL = "postgresql+psycopg://postgres:iHS8tmZYwyK65X@db:5432/phr"

# SQLAlchemy setup
engine = create_engine(DATABASE_URL)
Base = declarative_base()


# Define the database models
class Patient(Base):
    __tablename__ = 'patient'
    patient_uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    date_of_birth = Column(Date)
    gender = Column(String(10))
    email = Column(String(255))
    phone_number = Column(String(20))
    emergency_contact_name = Column(String(200))
    emergency_contact_relationship = Column(String(20))
    emergency_contact_number = Column(String(20))
    address = Column(Text)


class Doctor(Base):
    __tablename__ = 'doctor'
    doctor_uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    specialization = Column(String(255))
    email = Column(String(255))
    phone_number = Column(String(20))
    address = Column(Text)


class HealthRecord(Base):
    __tablename__ = 'health_record'
    record_uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_uuid = Column(UUID(as_uuid=True), ForeignKey('patient.patient_uuid'))
    doctor_uuid = Column(UUID(as_uuid=True), ForeignKey('doctor.doctor_uuid'))
    diagnosis = Column(Text)
    treatment = Column(Text)
    date = Column(Date)
    notes = Column(Text)


class Appointment(Base):
    __tablename__ = 'appointment'
    appointment_uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_uuid = Column(UUID(as_uuid=True), ForeignKey('patient.patient_uuid'))
    doctor_uuid = Column(UUID(as_uuid=True), ForeignKey('doctor.doctor_uuid'))
    date = Column(Date)
    time = Column(String(8))
    location = Column(String(255))
    status = Column(String(20))


class Medication(Base):
    __tablename__ = 'medication'
    medication_uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    manufacturer = Column(String(255))
    inventory = Column(Integer, default=0)


class Prescription(Base):
    __tablename__ = 'prescription'
    prescription_uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    doctor_uuid = Column(UUID(as_uuid=True), ForeignKey('doctor.doctor_uuid'))
    patient_uuid = Column(UUID(as_uuid=True), ForeignKey('patient.patient_uuid'))
    medication_uuid = Column(UUID(as_uuid=True), ForeignKey('medication.medication_uuid'))
    dosage = Column(String(50))
    frequency = Column(String(50))
    start_date = Column(Date)
    end_date = Column(Date)
    notes = Column(Text)


# Create tables
Base.metadata.create_all(bind=engine)
