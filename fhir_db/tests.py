from django.test import TestCase
from fhir_db.models import *
import uuid


class FhirTestCase(TestCase):
    def setUp(self):
        patient1_uuid = str(uuid.uuid4())
        Patient.objects.create(id=patient1_uuid, family_name="family_test", given_names="test given name")
