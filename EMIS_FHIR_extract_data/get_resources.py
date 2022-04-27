from os import listdir
import json
from fhir.resources.patient import Patient
from fhir.resources.encounter import Encounter
from fhir.resources.condition import Condition
from fhir.resources.claim import Claim
from fhir.resources.explanationofbenefit import ExplanationOfBenefit

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
    # def __int__(self, id, prefix, family_name, given_names, dob, gender, contact_number, address_line, address_city,
    #             address_district, address_state, address_postal_code, address_country, medical_record_number,
    #             social_security_number, drivers_licence, passport_number, maiden_name, marital_status):
    #     self.id = id
    #     self.prefix = prefix
    #     self.given_names = given_names
    #     self.family_name = family_name
    #     self.maiden_name = maiden_name
    #     self.dob = dob
    #     self.gender = gender
    #     self.contact_number = contact_number
    #     self.address_line = address_line
    #     self.address_city = address_city
    #     self.address_district = address_district
    #     self.address_state = address_state
    #     self.address_postal_code = address_postal_code
    #     self.address_country = address_country
    #     self.medical_record_number = medical_record_number
    #     self.social_security_number = social_security_number
    #     self.drivers_licence = drivers_licence
    #     self.passport_number = passport_number
    #     self.marital_status = marital_status

    def __init__(self):
        self.id = None
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

    def get_patient_obj(self, patient_resource):
        # patient = PatientResource()
        self.id = patient_resource.id
        patient_name_array = patient_resource.name
        for n in patient_name_array:
            if n.use == "official":
                if n.prefix is not None:
                    self.prefix = ', '.join(n.prefix)
                self.family_name = n.family
                self.given_names = ' '.join(n.given)
            elif n.use == "maiden":
                self.maiden_name = n.family

        self.dob = patient_resource.birthDate
        self.gender = patient_resource.gender

        patient_telecom_obj = patient_resource.telecom[0]
        self.contact_number = patient_telecom_obj.value

        patient_address_obj = patient_resource.address[0]
        self.address_line = ', '.join(patient_address_obj.line)
        self.address_city = patient_address_obj.city
        self.address_district = patient_address_obj.district
        self.address_state = patient_address_obj.state
        self.address_postal_code = patient_address_obj.postalCode
        self.address_country = patient_address_obj.country

        patient_identifiers = patient_resource.identifier
        for i in patient_identifiers:
            if i.type is None:
                continue
            if i.type.text == "Medical Record Number":
                self.medical_record_number = i.value
            elif i.type.text == "Social Security Number":
                self.social_security_number = i.value
            elif i.type.text == "Driver's License":
                self.drivers_licence = i.value
            elif i.type.text == "Passport Number":
                self.passport_number = i.value

        patient_marital_obj = patient_resource.maritalStatus
        if patient_marital_obj is not None:
            self.marital_status = marital_status_dict[patient_marital_obj.coding[0].code]

        return self

    def __str__(self):
        return f"id {self.id}\n" \
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
        self.id = None
        self.status = None
        self.patient_id = None
        self.encounter_class = None
        self.encounter_type = None
        self.primary_performer = None
        self.start_datetime = None
        self.end_datetime = None
        self.discharge_disposition = None
        self.location = None
        self.service_provider = None
        self.reason = None

    def get_encounter_obj(self, encounter_resource):
        # encounter = EncounterResource()
        self.id = encounter_resource.id
        self.status = encounter_resource.status

        subject_ref = encounter_resource.subject.reference
        self.patient_id = subject_ref.split(":")[2]

        self.encounter_class = encounter_class_dict[encounter_resource.class_fhir.code]
        self.encounter_type = encounter_resource.type[0].text
        self.primary_performer = encounter_resource.participant[0].individual.display
        self.start_datetime = encounter_resource.period.start
        self.end_datetime = encounter_resource.period.end

        if encounter_resource.hospitalization is not None:
            self.discharge_disposition = encounter_resource.hospitalization.dischargeDisposition.text

        self.location = encounter_resource.location[0].location.display
        self.service_provider = encounter_resource.serviceProvider.display

        if encounter_resource.reasonCode is not None:
            self.reason = encounter_resource.reasonCode[0].coding[0].display

        return self

    def __str__(self):
        return f"id: {self.id}\n" \
               f"status: {self.status}\n" \
               f"subject ID: {self.patient_id}\n" \
               f"class: {self.encounter_class}\n" \
               f"type: {self.encounter_type}\n" \
               f"primary performer: {self.primary_performer}\n" \
               f"start: {self.start_datetime}\n" \
               f"end: {self.end_datetime}\n" \
               f"discharge: {self.discharge_disposition}\n" \
               f"location: {self.location}\n" \
               f"service provider: {self.service_provider}\n" \
               f"reason: {self.reason}\n"


class ConditionResource:

    def __init__(self):
        self.id = None
        self.clinical_status = None
        self.verification_status = None
        self.category = None
        self.severity = None
        self.diagnosis = None
        self.body_site = None
        self.patient_id = None
        self.encounter_id = None
        self.onset_datetime = None
        self.record_datetime = None
        self.abatement_datetime = None

    def get_condition_obj(self, condition_resource):
        self.id = condition_resource.id
        self.clinical_status = condition_resource.clinicalStatus.coding[0].code
        self.verification_status = condition_resource.verificationStatus.coding[0].code
        self.category = condition_resource.category[0].coding[0].display

        if condition_resource.severity is not None:
            self.severity = condition_resource.severity.coding[0].display

        self.diagnosis = condition_resource.code.text

        if condition_resource.bodySite is not None:
            self.body_site = condition_resource

        subject_ref = condition_resource.subject.reference
        self.patient_id = subject_ref.split(":")[2]

        encounter_ref = condition_resource.encounter.reference
        self.encounter_id = encounter_ref.split(":")[2]

        self.onset_datetime = condition_resource.onsetDateTime
        self.record_datetime = condition_resource.recordedDate

        if condition_resource.abatementDateTime is not None:
            self.abatement_datetime = condition_resource.abatementDateTime
        return self


class ExplanationOfBenefitResource:
    def __init__(self):
        self.id = None
        self.status = None
        self.type = None
        self.use = None
        self.patient_id = None
        self.billable_start_datetime = None
        self.billable_end_datetime = None
        self.created = None
        self.insurance = None
        self.facility = None
        self.claim_id = None
        self.outcome = None
        self.encounter_id = None
        self.total_amount = None
        self.total_currency = None
        self.payment_amount = None
        self.payment_currency = None

    def get_explanation_of_benefit_obj(self, explanation_of_benefit):
        self.id = explanation_of_benefit.id
        self.status = explanation_of_benefit.status
        self.type = explanation_of_benefit.type.coding[0].code
        self.use = explanation_of_benefit.use

        patient_ref = explanation_of_benefit.patient.reference
        self.patient_id = patient_ref.split(":")[2]

        self.billable_start_datetime = explanation_of_benefit.billablePeriod.start
        self.billable_end_datetime = explanation_of_benefit.billablePeriod.end
        self.created = explanation_of_benefit.created
        self.insurance = explanation_of_benefit.insurance[0].coverage.display
        self.facility = explanation_of_benefit.facility.display

        claim_ref = explanation_of_benefit.claim.reference
        self.claim_id = claim_ref.split(":")[2]

        self.outcome = explanation_of_benefit.outcome

        encounter_ref = explanation_of_benefit.item[0].encounter[0].reference
        self.encounter_id = encounter_ref.split(":")[2]

        self.total_amount = explanation_of_benefit.total[0].amount.value
        self.total_currency = explanation_of_benefit.total[0].amount.currency
        self.payment_amount = explanation_of_benefit.payment.amount.value
        self.payment_currency = explanation_of_benefit.payment.amount.currency

        return self


def read_json(f_name):
    global entry
    # print(f_name)

    with open(f_name, 'r') as fhir_file:
        data = json.loads(fhir_file.read())
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

                pr = PatientResource()
                patient_obj = pr.get_patient_obj(patient)
                # print(patient_obj)
                # family_name = patient.name[0].telecom
                # if patient.telecom[0].use == "home":
                # if patient.address[0].text is not None:
                # if len(patient.name) > 1:
                #     print(patient.name[1])
                #     entry += 1
            elif res_type == "Encounter":
                encounter = Encounter.parse_obj(res)
                er = EncounterResource()
                encounter_obj = er.get_encounter_obj(encounter)
                # print(encounter_obj)
                # if encounter.participant[0].individual.display:
                # if encounter.reasonCode is not None:
                #     # print(encounter.hospitalization)
                #     # if len(encounter.hospitalization.dischargeDisposition.coding) > 0:
                #     #     print(f_name)
                #     #     print(encounter.hospitalization.dischargeDisposition.coding[0].display)
                #     #     print(encounter.hospitalization.dischargeDisposition.coding[0].code)
                #     entry += 1
            elif res_type == "Condition":
                condition = Condition.parse_obj(res)
                cr = ConditionResource()
                condition_obj = cr.get_condition_obj(condition)
                # print(condition_obj)
                # print(condition.clinicalStatus.coding[0].code)
                # if len(condition.category) > 0:
                # if condition.bodySite is not None:
                #     entry += 1

            elif res_type == "Claim":
                claim = Claim.parse_obj(res)
                # if claim.insurance[0].coverage.display == 'NO_INSURANCE':
                #     entry += 1
                # else:
                # print(claim.insurance[0].coverage.display)

            elif res_type == "ExplanationOfBenefit":
                explanation_of_benefit = ExplanationOfBenefit.parse_obj(res)
                eob_r = ExplanationOfBenefitResource()
                eob_obj = eob_r.get_explanation_of_benefit_obj(explanation_of_benefit)
                print(eob_obj)
                # print(explanation_of_benefit.insurer.display)
                # if explanation_of_benefit.item[0].encounter[0].reference is not None:
                # if len(explanation_of_benefit.type.coding) > 0:
                #     entry += 1

            resource_type.add(i["resource"]["resourceType"])


for f in dir_list:
    path = "./data/" + f
    read_json(path)

# print(resource_type)
print(entry)
print(resource_dict)
