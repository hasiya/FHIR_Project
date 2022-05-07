import json
import os
import sys

sys.path.append('')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FHIR_Project.settings')
import django
from django.contrib.auth import get_user_model

django.setup()
from django.contrib.auth.models import Permission
from fhir_db.models import *

from fhir.resources.patient import Patient as ResourcePatient
from fhir.resources.encounter import Encounter as ResourceEncounter
from fhir.resources.condition import Condition as ResourceCondition
from fhir.resources.explanationofbenefit import ExplanationOfBenefit as ResourceEOB

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
    patient_django = None
    encounter_django = None

    with open(f_name, 'r') as fhir_file:
        data = json.loads(fhir_file.read())
        print(f_name + " --- Processing")
        for i in data["entry"]:
            res_type = i["resource"]["resourceType"]
            res = i["resource"]

            if res_type == "Patient":
                patient = ResourcePatient.parse_obj(res)

                pr = PatientResource()
                patient_obj = pr.get_patient_obj(patient)
                # check if the patient exist before adding
                if Patient.objects.filter(id=patient_obj.id).exists():
                    patient_django = Patient.objects.get(id=patient_obj.id)
                    print("\tpatient Exists")
                else:
                    patient_django = Patient(
                        id=patient_obj.id,
                        prefix=patient_obj.prefix,
                        given_names=patient_obj.given_names,
                        family_name=patient_obj.family_name,
                        maiden_name=patient_obj.maiden_name,
                        birth_date=patient_obj.dob,
                        gender=patient_obj.gender,
                        marital_status=patient_obj.marital_status,
                        contact_number=patient_obj.contact_number,
                        address_line=patient_obj.address_line,
                        address_city=patient_obj.address_city,
                        address_district=patient_obj.address_district,
                        address_state=patient_obj.address_state,
                        address_postal_code=patient_obj.address_postal_code,
                        address_country=patient_obj.address_country,
                        medical_record_number=patient_obj.medical_record_number,
                        social_security_number=patient_obj.social_security_number,
                        drivers_licence=patient_obj.drivers_licence,
                        passport_number=patient_obj.passport_number
                    )
                    patient_django.save()
                    print("\tPatient Saved")

            elif res_type == "Encounter":
                encounter = ResourceEncounter.parse_obj(res)
                er = EncounterResource()
                encounter_obj = er.get_encounter_obj(encounter)
                if Encounter.objects.filter(id=encounter_obj.id).exists():
                    encounter_django = Encounter.objects.get(id=encounter_obj.id)
                    print("\tEncounter Exists")
                else:
                    encounter_django = Encounter(
                        id=encounter_obj.id,
                        patient=patient_django,
                        status=encounter_obj.status,
                        encounter_class=encounter_obj.encounter_class,
                        encounter_type=encounter_obj.encounter_type,
                        primary_performer=encounter_obj.primary_performer,
                        start_datetime=encounter_obj.start_datetime,
                        end_datetime=encounter_obj.end_datetime,
                        discharge_disposition=encounter_obj.discharge_disposition,
                        location=encounter_obj.location,
                        service_provider=encounter_obj.service_provider,
                        reason=encounter_obj.reason
                    )
                    encounter_django.save()
                    print("\tEncounter Saved")

            elif res_type == "Condition":
                condition = ResourceCondition.parse_obj(res)
                cr = ConditionResource()
                condition_obj = cr.get_condition_obj(condition)
                if Condition.objects.filter(id=condition_obj.id).exists():
                    condition_django = Condition.objects.get(id=condition_obj.id)
                    print("Condition Exists")
                else:
                    condition_django = Condition(
                        id=condition_obj.id,
                        patient=patient_django,
                        encounter=encounter_django,
                        clinical_status=condition_obj.clinical_status,
                        severity=condition_obj.severity,
                        diagnosis=condition_obj.diagnosis,
                        body_site=condition_obj.body_site,
                        onset_datetime=condition_obj.onset_datetime,
                        record_datetime=condition_obj.record_datetime,
                        abatement_datetime=condition_obj.abatement_datetime
                    )
                    condition_django.save()
                    print("\tCondition Saved")

            elif res_type == "ExplanationOfBenefit":
                explanation_of_benefit = ResourceEOB.parse_obj(res)
                eob_r = ExplanationOfBenefitResource()
                eob_obj = eob_r.get_explanation_of_benefit_obj(explanation_of_benefit)
                if ExplanationOfBenefit.objects.filter(id=eob_obj.id):
                    eob_django = ExplanationOfBenefit.objects.get(id=eob_obj.id)
                    print("Explanation Of Benefit Exists")
                else:
                    eob_django = ExplanationOfBenefit(
                        id=eob_obj.id,
                        patient=patient_django,
                        encounter=encounter_django,
                        status=eob_obj.status,
                        type=eob_obj.type,
                        use=eob_obj.use,
                        billable_start_datetime=eob_obj.billable_start_datetime,
                        billable_end_datetime=eob_obj.billable_end_datetime,
                        created=eob_obj.created,
                        insurance=eob_obj.insurance,
                        facility=eob_obj.facility,
                        claim_id=eob_obj.claim_id,
                        outcome=eob_obj.outcome,
                        total_amount=eob_obj.total_amount,
                        total_currency=eob_obj.total_currency,
                        payment_amount=eob_obj.payment_amount,
                        payment_currency=eob_obj.payment_currency
                    )
                    eob_django.save()
                    print("\tExplanation Of Benefit Saved")


def empty_db():
    if Patient.objects.all().count() > 1:
        Patient.objects.all().delete()
        print("Patient data deleted")
    else:
        print("Patient data is already empty")

    if Encounter.objects.all().count() > 1:
        Encounter.objects.all().delete()
        print("Encounter data deleted")
    else:
        print("Encounter data is already empty")

    if Condition.objects.all().count() > 1:
        Condition.objects.all().delete()
        print("Condition data deleted")
    else:
        print("Encounter data is already empty")

    if ExplanationOfBenefit.objects.all().count() > 1:
        ExplanationOfBenefit.objects.all().delete()
        print("Explanation Of Benefit data deleted")
    else:
        print("Explanation Of Benefit data is already empty")


def create_admin_user():
    User = get_user_model()
    username = "user"
    password = "pwd"
    if not User.objects.filter(username=username).exists():
        user = User.objects.create_user(username=username, password=password)
        user.is_superuser = False
        user.is_staff = True
        user.save()

        permission_explanationofbenefit = Permission.objects.get(codename="view_explanationofbenefit")
        permission_patient = Permission.objects.get(codename="view_patient")
        permission_encounter = Permission.objects.get(codename="view_encounter")
        permission_condition = Permission.objects.get(codename="view_condition")

        user.user_permissions.add(permission_explanationofbenefit)
        user.user_permissions.add(permission_patient)
        user.user_permissions.add(permission_encounter)
        user.user_permissions.add(permission_condition)

        print("Admin user created with permission to view FHIR Data")
        print(f"\tUsername - {username}")
        print(f"\tPassword - {password}")
    else:
        print("Admin user already exists")
        print(f"\tUsername - {username}")
        print(f"\tPassword - {password}")


def populate_db():
    data_path = './EMIS_FHIR_extract_data/data/'
    dir_list = os.listdir(data_path)
    if Patient.objects.all().count() == 0:
        for f in dir_list:
            path = data_path + f
            read_json(path)
            print(path + " --- added to the Database")
    else:
        print("The Database already contains data...")
