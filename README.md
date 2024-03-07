# PHR System with RESTful API

## Overview

This project is a Personal Health Record (PHR) system with a RESTful API. The system uses PostgreSQL as its database. This API provides functionalities to manage patients, doctors, health records, medications, appointments, and prescriptions.

You can set up this project using `docker-compose`.

## Data Models

The database is modeled as follows:

### patient

| Field                        | Type          | Constraints                             |
|------------------------------|---------------|-----------------------------------------|
| patient_uuid                 | UUID          | DEFAULT uuid_generate_v4() PRIMARY KEY |
| first_name                   | VARCHAR(100)  | NOT NULL                                |
| last_name                    | VARCHAR(100)  | NOT NULL                                |
| date_of_birth                | DATE          |                                         |
| gender                       | VARCHAR(10)   |                                         |
| email                        | VARCHAR(255)  |                                         |
| phone_number                 | VARCHAR(20)   |                                         |
| emergency_contact_name       | VARCHAR(200)  |                                         |
| emergency_contact_relationship| VARCHAR(20)   |                                         |
| emergency_contact_number     | VARCHAR(20)   |                                         |
| address                      | TEXT          |                                         |

### doctor

| Field            | Type          | Constraints                             |
|------------------|---------------|-----------------------------------------|
| doctor_uuid      | UUID          | DEFAULT uuid_generate_v4() PRIMARY KEY |
| first_name       | VARCHAR(100)  | NOT NULL                                |
| last_name        | VARCHAR(100)  | NOT NULL                                |
| specialization   | VARCHAR(255)  |                                         |
| email            | VARCHAR(255)  |                                         |
| phone_number     | VARCHAR(20)   |                                         |
| address          | TEXT          |                                         |

### health_record

| Field            | Type          | Constraints                             |
|------------------|---------------|-----------------------------------------|
| record_uuid      | UUID          | DEFAULT uuid_generate_v4() PRIMARY KEY |
| patient_uuid     | UUID          | REFERENCES patient(patient_uuid)       |
| doctor_uuid      | UUID          | REFERENCES doctor(doctor_uuid)         |
| diagnosis        | TEXT          |                                         |
| treatment        | TEXT          |                                         |
| date             | DATE          |                                         |
| notes            | TEXT          |                                         |

### appointment

| Field              | Type          | Constraints                             |
|--------------------|---------------|-----------------------------------------|
| appointment_uuid   | UUID          | DEFAULT uuid_generate_v4() PRIMARY KEY |
| patient_uuid       | UUID          | REFERENCES patient(patient_uuid)       |
| doctor_uuid        | UUID          | REFERENCES doctor(doctor_uuid)         |
| date               | DATE          |                                         |
| time               | VARCHAR(8)    |                                         |
| location           | VARCHAR(255)  |                                         |
| status             | VARCHAR(20)   |                                         |


### medication

| Field              | Type          | Constraints                             |
|--------------------|---------------|-----------------------------------------|
| medication_uuid    | UUID          | DEFAULT uuid_generate_v4() PRIMARY KEY |
| name               | VARCHAR(255)  | NOT NULL                                |
| manufacturer       | VARCHAR(255)  |                                         |
| inventory          | INTEGER       | DEFAULT 0                               |


### prescription

| Field              | Type          | Constraints                             |
|--------------------|---------------|-----------------------------------------|
| prescription_uuid  | UUID          | DEFAULT uuid_generate_v4() PRIMARY KEY |
| doctor_uuid        | UUID          | REFERENCES doctor(doctor_uuid)         |
| patient_uuid       | UUID          | REFERENCES patient(patient_uuid)       |
| medication_uuid    | UUID          | REFERENCES medication(medication_uuid) |
| dosage             | VARCHAR(50)   |                                         |
| frequency          | VARCHAR(50)   |                                         |
| start_date         | DATE          |                                         |
| end_date           | DATE          |                                         |
| notes              | TEXT          |                                         |


## Setup

### Reverse Proxy (Optional)

A Nginx reverse proxy is included with minimal configuration. By default, the proxy listens on `port 80`. Modify the `nginx.conf` file if needed. TLS is highly recommended for necessary security.

### docker-compose

The default username is `admin`, and the password is `password`. It is strongly recommended that you use a safe password. To change the username and password, add the following environment variables to the `docker-compose.yml` file:

```
# docker-compose.yml

services:
  api:
    environment:
      API_USERNAME: admin
      API_PASSWORD: password
```

Then, to build the server: `docker-compose build`

Finally, to run the server: `docker-compose up -d`

## Usage

### Authentication

The API requires authentication to access certain endpoints. Ensure that you include the necessary authentication headers in your requests.

### Endpoints

### 1. Get All Entities

#### 1.1 Get All Patients

- **Endpoint:** `/patients`
- **Method:** `GET`
- **Parameters:** None
- **Response:**
  - Status Code: 200 OK
  - Content Type: `application/json`
  - Body: List of patient entities

#### 1.2 Get All Doctors

- **Endpoint:** `/doctors`
- **Method:** `GET`
- **Parameters:** None
- **Response:**
  - Status Code: 200 OK
  - Content Type: `application/json`
  - Body: List of doctor entities

#### 1.3 Get All Health Records

- **Endpoint:** `/health-records`
- **Method:** `GET`
- **Parameters:** None
- **Response:**
  - Status Code: 200 OK
  - Content Type: `application/json`
  - Body: List of health record entities

#### 1.4 Get All Medications

- **Endpoint:** `/medications`
- **Method:** `GET`
- **Parameters:** None
- **Response:**
  - Status Code: 200 OK
  - Content Type: `application/json`
  - Body: List of medication entities

#### 1.5 Get All Appointments

- **Endpoint:** `/appointments`
- **Method:** `GET`
- **Parameters:** None
- **Response:**
  - Status Code: 200 OK
  - Content Type: `application/json`
  - Body: List of appointment entities

#### 1.6 Get All Prescriptions

- **Endpoint:** `/prescriptions`
- **Method:** `GET`
- **Parameters:** None
- **Response:**
  - Status Code: 200 OK
  - Content Type: `application/json`
  - Body: List of prescription entities

### 2. Get Entities by Foreign Key

#### 2.1 Get Appointments by Patient UUID

- **Endpoint:** `/appointments/by-patient/{patient_uuid}`
- **Method:** `GET`
- **Parameters:**
  - `patient_uuid`: UUID of the patient
- **Response:**
  - Status Code: 200 OK
  - Content Type: `application/json`
  - Body: List of appointment entities for the specified patient

#### 2.2 Get Appointments by Doctor UUID

- **Endpoint:** `/appointments/by-doctor/{doctor_uuid}`
- **Method:** `GET`
- **Parameters:**
  - `doctor_uuid`: UUID of the doctor
- **Response:**
  - Status Code: 200 OK
  - Content Type: `application/json`
  - Body: List of appointment entities for the specified doctor

#### 2.3 Get Prescriptions by Patient UUID

- **Endpoint:** `/prescriptions/by-patient/{patient_uuid}`
- **Method:** `GET`
- **Parameters:**
  - `patient_uuid`: UUID of the patient
- **Response:**
  - Status Code: 200 OK
  - Content Type: `application/json`
  - Body: List of prescription entities for the specified patient

#### 2.4 Get Prescriptions by Doctor UUID

- **Endpoint:** `/prescriptions/by-doctor/{doctor_uuid}`
- **Method:** `GET`
- **Parameters:**
  - `doctor_uuid`: UUID of the doctor
- **Response:**
  - Status Code: 200 OK
  - Content Type: `application/json`
  - Body: List of prescription entities for the specified doctor

#### 2.5 Get Prescriptions by Medication UUID

- **Endpoint:** `/prescriptions/by-medication/{medication_uuid}`
- **Method:** `GET`
- **Parameters:**
  - `medication_uuid`: UUID of the medication
- **Response:**
  - Status Code: 200 OK
  - Content Type: `application/json`
  - Body: List of prescription entities for the specified medication

### 3. Get Specific Entity by UUID

#### 3.1 Get Patient by UUID

- **Endpoint:** `/patients/{patient_uuid}`
- **Method:** `GET`
- **Parameters:**
  - `patient_uuid`: UUID of the patient
- **Response:**
  - Status Code: 200 OK
  - Content Type: `application/json`
  - Body: Patient entity for the specified UUID

#### 3.2 Get Doctor by UUID

- **Endpoint:** `/doctors/{doctor_uuid}`
- **Method:** `GET`
- **Parameters:**
  - `doctor_uuid`: UUID of the doctor
- **Response:**
  - Status Code: 200 OK
  - Content Type: `application/json`
  - Body: Doctor entity for the specified UUID

#### 3.3 Get Health Record by UUID

- **Endpoint:** `/health-records/{health_record_uuid}`
- **Method:** `GET`
- **Parameters:**
  - `health_record_uuid`: UUID of the health record
- **Response:**
  - Status Code: 200 OK
  - Content Type: `application/json`
  - Body: Health record entity for the specified UUID

#### 3.4 Get Medication by UUID

- **Endpoint:** `/medications/{medication_uuid}`
- **Method:** `GET`
- **Parameters:**
  - `medication_uuid`: UUID of the medication
- **Response:**
  - Status Code: 200 OK
  - Content Type: `application/json`
  - Body: Medication entity for the specified UUID

#### 3.5 Get Appointment by UUID

- **Endpoint:** `/appointments/{appointment_uuid}`
- **Method:** `GET`
- **Parameters:**
  - `appointment_uuid`: UUID of the appointment
- **Response:**
  - Status Code: 200 OK
  - Content Type: `application/json`
  - Body: Appointment entity for the specified UUID

#### 3.6 Get Prescription by UUID

- **Endpoint:** `/prescriptions/{prescription_uuid}`
- **Method:** `GET`
- **Parameters:**
  - `prescription_uuid`: UUID of the prescription
- **Response:**
  - Status Code: 200 OK
  - Content Type: `application/json`
  - Body: Prescription entity for the specified UUID

### 4. Create New Entity

#### 4.1 Create New Patient

- **Endpoint:** `/patients`
- **Method:** `POST`
- **Parameters:** JSON payload with patient data
- **Response:**
  - Status Code: 201 Created
  - Content Type: `text/plain`
  - Body: "New patient created"

#### 4.2 Create New Doctor

- **Endpoint:** `/doctors`
- **Method:** `POST`
- **Parameters:** JSON payload with doctor data
- **Response:**
  - Status Code: 201 Created
  - Content Type: `text/plain`
  - Body: "New doctor created"

#### 4.3 Create New Health Record

- **Endpoint:** `/health-records`
- **Method:** `POST`
- **Parameters:** JSON payload with health record data
- **Response:**
  - Status Code: 201 Created
  - Content Type: `text/plain`
  - Body: "New health record created"

#### 4.4 Create New Medication

- **Endpoint:** `/medications`
- **Method:** `POST`
- **Parameters:** JSON payload with medication data
- **Response:**
  - Status Code: 201 Created
  - Content Type: `text/plain`
  - Body: "New medication created"

#### 4.5 Create New Appointment

- **Endpoint:** `/appointments`
- **Method:** `POST`
- **Parameters:** JSON payload with appointment data
- **Response:**
  - Status Code: 201 Created
  - Content Type: `text/plain`
  - Body: "New appointment created"

#### 4.6 Create New Prescription

- **Endpoint:** `/prescriptions`
- **Method:** `POST`
- **Parameters:** JSON payload with prescription data
- **Response:**
  - Status Code: 201 Created
  - Content Type: `text/plain`
  - Body: "New prescription created"

### 5. Update Entity

#### 5.1 Update Patient

- **Endpoint:** `/patients/{patient_uuid}`
- **Method:** `PUT`
- **Parameters:**
  - `patient_uuid`: UUID of the patient to update
- **Request Body:** JSON payload with updated patient data
- **Response:**
  - Status Code: 200 OK
  - Content Type: `text/plain`
  - Body: "Patient updated"

#### 5.2 Update Doctor

- **Endpoint:** `/doctors/{doctor_uuid}`
- **Method:** `PUT`
- **Parameters:**
  - `doctor_uuid`: UUID of the doctor to update
- **Request Body:** JSON payload with updated doctor data
- **Response:**
  - Status Code: 200 OK
  - Content Type: `text/plain`
  - Body: "Doctor updated"

#### 5.3 Update Health Record

- **Endpoint:** `/health-records/{health_record_uuid}`
- **Method:** `PUT`
- **Parameters:**
  - `health_record_uuid`: UUID of the health record to update
- **Request Body:** JSON payload with updated health record data
- **Response:**
  - Status Code: 200 OK
  - Content Type: `text/plain`
  - Body: "Health record updated"

#### 5.4 Update Medication

- **Endpoint:** `/medications/{medication_uuid}`
- **Method:** `PUT`
- **Parameters:**
  - `medication_uuid`: UUID of the medication to update
- **Request Body:** JSON payload with updated medication data
- **Response:**
  - Status Code: 200 OK
  - Content Type: `text/plain`
  - Body: "Medication updated"

#### 5.5 Update Appointment

- **Endpoint:** `/appointments/{appointment_uuid}`
- **Method:** `PUT`
- **Parameters:**
  - `appointment_uuid`: UUID of the appointment to update
- **Request Body:** JSON payload with updated appointment data
- **Response:**
  - Status Code: 200 OK
  - Content Type: `text/plain`
  - Body: "Appointment updated"

#### 5.6 Update Prescription

- **Endpoint:** `/prescriptions/{prescription_uuid}`
- **Method:** `PUT`
- **Parameters:**
  - `prescription_uuid`: UUID of the prescription to update
- **Request Body:** JSON payload with updated prescription data
- **Response:**
  - Status Code: 200 OK
  - Content Type: `text/plain`
  - Body: "Prescription updated"

### 6. Delete Entity

#### 6.1 Delete Patient

- **Endpoint:** `/patients/{patient_uuid}`
- **Method:** `DELETE`
- **Parameters:**
  - `patient_uuid`: UUID of the patient to delete
- **Response:**
  - Status Code: 200 OK
  - Content Type: `text/plain`
  - Body: "Patient deleted"

#### 6.2 Delete Doctor

- **Endpoint:** `/doctors/{doctor_uuid}`
- **Method:** `DELETE`
- **Parameters:**
  - `doctor_uuid`: UUID of the doctor to delete
- **Response:**
  - Status Code: 200 OK
  - Content Type: `text/plain`
  - Body: "Doctor deleted"

#### 6.3 Delete Health Record

- **Endpoint:** `/health-records/{health_record_uuid}`
- **Method:** `DELETE`
- **Parameters:**
  - `health_record_uuid`: UUID of the health record to delete
- **Response:**
  - Status Code: 200 OK
  - Content Type: `text/plain`
  - Body: "Health record deleted"

#### 6.4 Delete Medication

- **Endpoint:** `/medications/{medication_uuid}`
- **Method:** `DELETE`
- **Parameters:**
  - `medication_uuid`: UUID of the medication to delete
- **Response:**
  - Status Code: 200 OK
  - Content Type: `text/plain`
  - Body: "Medication deleted"

#### 6.5 Delete Appointment

- **Endpoint:** `/appointments/{appointment_uuid}`
- **Method:** `DELETE`
- **Parameters:**
  - `appointment_uuid`: UUID of the appointment to delete
- **Response:**
  - Status Code: 200 OK
  - Content Type: `text/plain`
  - Body: "Appointment deleted"

#### 6.6 Delete Prescription

- **Endpoint:** `/prescriptions/{prescription_uuid}`
- **Method:** `DELETE`
- **Parameters:**
  - `prescription_uuid`: UUID of the prescription to delete
- **Response:**
  - Status Code: 200 OK
  - Content Type: `text/plain`
  - Body: "Prescription deleted"
