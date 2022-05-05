from django import forms
from django.core.validators import FileExtensionValidator


class UploadFileForm(forms.Form):
    files = forms.FileField(label="Upload FHIR JSON files...",
                            widget=forms.ClearableFileInput(attrs={'multiple': True}))
