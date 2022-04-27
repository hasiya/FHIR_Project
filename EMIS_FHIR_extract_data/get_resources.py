from os import listdir
import json
from fhir.resources.patient import Patient
from fhir.resources.encounter import Encounter

dir_list = listdir("./data")
resource_type = set()
person_array = []
resource_dict = {}

entry = 0

marital_status_dict = {
    "A": "Annulled",
    "D": "Divorced",
    "I": "Interlocutory",
    "L": "Legally Separated",
    "M": "Married",
    "P": "Polygamous",
    "S": "Never Married",
    "T": "Domestic partner",
    "U": "Unmarried",
    "W": "Widowed",
    "UNK": "Unknown"
}

encounter_class_dict = {
    "AMB": "Ambulatory",
    "EMER": "Emergency",
    "FLD": "Field",
    "HH": "Home Health",
    "IMP": "Inpatient Encounter",
    "ACUTE": "Inpatient Acute",
    "NONAC": "Inpatient Non-Acute",
    "OBSENC": "Observation Encounter",
    "PRENC": "Pre-Admission",
    "SS": "sShort Stay",
    "VR": "Virtual"
}


class PatientResource:
    def __int__(self, uuid, prefix, family_name, given_names, dob, gender, contact_number, address_line, address_city,
                address_district, address_state, address_postal_code, address_country, medical_record_number,
                social_security_number, drivers_licence, passport_number, maiden_name, marital_status):
        self.uuid = uuid
        self.prefix = prefix
        self.given_names = given_names
        self.family_name = family_name
        self.maiden_name = maiden_name
        self.dob = dob
        self.gender = gender
        self.contact_number = contact_number
        self.address_line = address_line
        self.address_city = address_city
        self.address_district = address_district
        self.address_state = address_state
        self.address_postal_code = address_postal_code
        self.address_country = address_country
        self.medical_record_number = medical_record_number
        self.social_security_number = social_security_number
        self.drivers_licence = drivers_licence
        self.passport_number = passport_number
        self.marital_status = marital_status

    def __init__(self):
        self.uuid = None
        self.prefix = None
        self.given_names = None
        self.family_name = None
        self.maiden_name = None
        self.dob = None
        self.gender = None
        self.contact_number = None
        self.address_line = None
        self.address_city = None
        self.address_district = None
        self.address_state = None
        self.address_postal_code = None
        self.address_country = None
        self.medical_record_number = None
        self.social_security_number = None
        self.drivers_licence = None
        self.passport_number = None
        self.marital_status = None

    def __str__(self):
        return f"id {self.uuid}\n" \
               f"Name: {self.prefix} {self.given_names} {self.family_name}\n" \
               f"Maiden Name: {self.maiden_name}\n" \
               f"DoB : {self.dob}\n" \
               f"Gender: {self.gender}\n" \
               f"contact: {self.contact_number}\n" \
               f"address: {self.address_line}, {self.address_city}, {self.address_district}, {self.address_state}, {self.address_postal_code}, {self.address_country}\n" \
               f"Medical Record: {self.medical_record_number}\n" \
               f"SS: {self.social_security_number}\n" \
               f"DL: {self.drivers_licence}\n" \
               f"PPN: {self.passport_number}\n" \
               f"Marital Status: {self.marital_status}\n"


class EncounterResource:
    def __init__(self):
        self.uuid = None
        self.status = None
        self.subject_uuid = None
        self.encounter_class = None
        self.encounter_type = None
        self.primary_performer = None
        self.start_datetime = None
        self.end_datetime = None
        self.discharge_disposition = None
        self.location = None
        self.service_provider = None
        self.reason = None

    def __str__(self):
        return f"id: {self.uuid}\n" \
               f"status: {self.status}\n" \
               f"subject ID: {self.subject_uuid}\n" \
               f"class: {self.encounter_class}\n" \
               f"type: {self.encounter_type}\n" \
               f"primary performer: {self.primary_performer}\n" \
               f"start: {self.start_datetime}\n" \
               f"end: {self.end_datetime}\n" \
               f"discharge: {self.discharge_disposition}\n" \
               f"location: {self.location}\n" \
               f"service provider: {self.service_provider}\n" \
               f"reason: {self.reason}\n"


def get_patient_obj(patient_resource):
    patient = PatientResource()
    patient.uuid = patient_resource.id
    patient_name_array = patient_resource.name
    for n in patient_name_array:
        if n.use == "official":
            if n.prefix is not None:
                patient.prefix = ', '.join(n.prefix)
            patient.family_name = n.family
            patient.given_names = ' '.join(n.given)
        elif n.use == "maiden":
            patient.maiden_name = n.family

    patient.dob = patient_resource.birthDate
    patient.gender = patient_resource.gender

    patient_telecom_obj = patient_resource.telecom[0]
    patient.contact_number = patient_telecom_obj.value

    patient_address_obj = patient_resource.address[0]
    patient.address_line = ', '.join(patient_address_obj.line)
    patient.address_city = patient_address_obj.city
    patient.address_district = patient_address_obj.district
    patient.address_state = patient_address_obj.state
    patient.address_postal_code = patient_address_obj.postalCode
    patient.address_country = patient_address_obj.country

    patient_identifiers = patient_resource.identifier
    for i in patient_identifiers:
        if i.type is None:
            continue
        if i.type.text == "Medical Record Number":
            patient.medical_record_number = i.value
        elif i.type.text == "Social Security Number":
            patient.social_security_number = i.value
        elif i.type.text == "Driver's License":
            patient.drivers_licence = i.value
        elif i.type.text == "Passport Number":
            patient.passport_number = i.value

    patient_marital_obj = patient_resource.maritalStatus
    if patient_marital_obj is not None:
        patient.marital_status = marital_status_dict[patient_marital_obj.coding[0].code]

    return patient


def get_encounter_obj(encounter_resource):
    encounter = EncounterResource()
    encounter.uuid = encounter_resource.id
    encounter.status = encounter_resource.status

    subject_ref = encounter_resource.subject.reference
    encounter.subject_uuid = subject_ref.split(":")[2]

    encounter.encounter_class = encounter_class_dict[encounter_resource.class_fhir.code]
    encounter.encounter_type = encounter_resource.type[0].text
    encounter.primary_performer = encounter_resource.participant[0].individual.display
    encounter.start_datetime = encounter_resource.period.start
    encounter.end_datetime = encounter_resource.period.end

    if encounter_resource.hospitalization is not None:
        encounter.discharge_disposition = encounter_resource.hospitalization.dischargeDisposition.text

    encounter.location = encounter_resource.location[0].location.display
    encounter.service_provider = encounter_resource.serviceProvider.display

    if encounter_resource.reasonCode is not None:
        encounter.reason = encounter_resource.reasonCode[0].coding[0].display

    return encounter


def read_json(f_name):
    global entry
    # print(f_name)

    with open(f_name, 'r') as F:
        person = {}
        data = json.loads(F.read())
        for i in data["entry"]:
            res_type = i["resource"]["resourceType"]
            res = i["resource"]
            if res_type in resource_type:
                val = resource_dict[res_type]
                val += 1
                resource_dict[res_type] = val
            else:
                resource_dict[res_type] = 1

            if res_type == "Patient":
                patient = Patient.parse_obj(res)

                patient_obj = get_patient_obj(patient)
                # print(patient_obj)
                # family_name = patient.name[0].telecom
                # if patient.telecom[0].use == "home":
                # if patient.address[0].text is not None:
                # if len(patient.name) > 1:
                #     print(patient.name[1])
                #     entry += 1
            elif res_type == "Encounter":
                encounter = Encounter.parse_obj(res)
                encounter_obj = get_encounter_obj(encounter)
                print(encounter_obj)
                # if encounter.participant[0].individual.display:
                if encounter.reasonCode is not None:
                    # print(encounter.hospitalization)
                    # if len(encounter.hospitalization.dischargeDisposition.coding) > 0:
                    #     print(f_name)
                    #     print(encounter.hospitalization.dischargeDisposition.coding[0].display)
                    #     print(encounter.hospitalization.dischargeDisposition.coding[0].code)
                    entry += 1
            # entry = entry + 1

            resource_type.add(i["resource"]["resourceType"])


# print(dir_list)
for f in dir_list:
    path = "./data/" + f
    read_json(path)

# print(resource_type)
print(entry)
print(resource_dict)
