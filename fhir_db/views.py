from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_protect
import json

from .forms import UploadFileForm
from fhir_db.lib import process_fhir


# Create your views here.

@csrf_protect
def index(request):
    # template = loader.get_template('fhir_db/index.html')
    template = 'fhir_db/index.html'
    form = UploadFileForm(request.POST, request.FILES)
    context = {
        'form': form,
        'processed_files': []
    }
    if request.method == 'POST':
        # form = UploadFileForm(request.POST, request.FILES)
        files = request.FILES.getlist('files')
        if form.is_valid():
            processed_files = []
            for f in files:
                process_fhir.read_json(f)
                processed_files.append(f.name)
                print(f)
            form = UploadFileForm()

            context = {
                'form': form,
                'processed_files': processed_files
            }
    else:
        form = UploadFileForm()
        context = {
            'form': form,
            'processed_files': []
        }

    return render(request, template, context)

# def process_files(request):
#     if request.method == 'GET':
#         # form = UploadFileForm(request.POST)
#         files = request.FILES.getlist('files')
#         # if form.is_valid():
#         for f in files:
#             print(f)
#
#     return HttpResponse("testing")
