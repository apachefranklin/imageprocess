from django.http import JsonResponse
from django.shortcuts import render
from django.http import HttpResponseRedirect

import os
from .form import UploadFileForm

# Create your views here.


def index(request):
    return render(request,"imageprocess/index.html")

def luminecance(request):
    return render(request,"imageprocess/luminecance.html")



# Imaginary function to handle an uploaded file.
def handle_uploaded_file(f):
    print(os.getcwd())
    with open('imageprocess/static/imageprocess/images/name.jpg', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return JsonResponse({"status":False})
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})
