from django.db import models


# Creating the Patient  Model class to create a database tabel for Patient resource data
class Patient(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    prefix = models.CharField(max_length=10, null=True)
    given_names = models.CharField(max_length=250)
    family_name = models.CharField(max_length=50)
    maiden_name = models.CharField(max_length=50, null=True)
    birth_date = models.DateField()
    gender = models.CharField(max_length=50)
    marital_status = models.CharField(max_length=25, null=True)
    contact_number = models.CharField(max_length=25, null=True)
    address_line = models.CharField(max_length=500, null=True)
    address_city = models.CharField(max_length=50, null=True)
    address_district = models.CharField(max_length=50, null=True)
    address_state = models.CharField(max_length=50, null=True)
    address_postal_code = models.CharField(max_length=20, null=True)
    address_country = models.CharField(max_length=50, null=True)
    medical_record_number = models.CharField(max_length=50, null=True)
    social_security_number = models.CharField(max_length=50, null=True)
    drivers_licence = models.CharField(max_length=50, null=True)
    passport_number = models.CharField(max_length=50, null=True)

    def __str__(self):
        return f"id {self.id}\n" \
               f"Name: {self.prefix} {self.given_names} {self.family_name}\n" \
               f"Maiden Name: {self.maiden_name}\n" \
               f"DoB : {self.birth_date}\n" \
               f"Gender: {self.gender}\n" \
               f"contact: {self.contact_number}\n" \
               f"address: {self.address_line}, {self.address_city}, {self.address_district}, {self.address_state}, {self.address_postal_code}, {self.address_country}\n" \
               f"Medical Record: {self.medical_record_number}\n" \
               f"SS: {self.social_security_number}\n" \
               f"DL: {self.drivers_licence}\n" \
               f"PPN: {self.passport_number}\n" \
               f"Marital Status: {self.marital_status}\n"


# Creating the Encounter Model class to create a database tabel for Encounter resource data
class Encounter(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    status = models.CharField(max_length=25)
    encounter_class = models.CharField(max_length=50, null=True)
    encounter_type = models.CharField(max_length=100, null=True)
    primary_performer = models.CharField(max_length=300, null=True)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    discharge_disposition = models.CharField(max_length=150, null=True)
    location = models.CharField(max_length=100, null=True)
    service_provider = models.CharField(max_length=100, null=True)
    reason = models.CharField(max_length=150, null=True)

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


# Creating the Condition Model class to create a database tabel for Condition resource data
class Condition(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    encounter = models.ForeignKey(Encounter, on_delete=models.CASCADE)
    clinical_status = models.CharField(max_length=20)
    severity = models.CharField(max_length=20, null=True)
    diagnosis = models.CharField(max_length=1000, null=True)
    body_site = models.CharField(max_length=500, null=True)
    onset_datetime = models.DateTimeField()
    record_datetime = models.DateTimeField()
    abatement_datetime = models.DateTimeField(null=True)


# Creating the Condition Model class to create a database tabel for Condition resource data
class ExplanationOfBenefit(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    encounter = models.ForeignKey(Encounter, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, null=True)
    type = models.CharField(max_length=25, null=True)
    use = models.CharField(max_length=25, null=True)
    billable_start_datetime = models.DateTimeField()
    billable_end_datetime = models.DateTimeField()
    created = models.DateTimeField()
    insurance = models.CharField(max_length=300, null=True)
    facility = models.CharField(max_length=300, null=True)
    claim_id = models.CharField(max_length=100, null=True)
    outcome = models.CharField(max_length=20, null=True)
    total_amount = models.DecimalField(max_digits=100, decimal_places=50, null=True)
    total_currency = models.CharField(max_length=5, null=True)
    payment_amount = models.DecimalField(max_digits=100, decimal_places=50, null=True)
    payment_currency = models.CharField(max_length=5, null=True)
