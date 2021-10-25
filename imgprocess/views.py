from django.http import JsonResponse
from django.shortcuts import render
from django.http import HttpResponseRedirect,FileResponse

import os
from .form import UploadFileForm
from .utils.img_lib import ImgLib
from .utils.utility import *
from PIL import Image
import numpy as np
# Create your views here.

def download_file(request):
    file_name=request.GET["download_name"]
    response =FileResponse(open(result_path+file_name,"r"))
    
    return response

def index(request):
    return render(request,"imgprocess/index.html")

def constraste(request):
    return render(request,"imgprocess/constraste.html")


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['imguploaded'],"")
            return JsonResponse({"status":False})
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})

#vu egalisation de l'histogramme

def egalisation_histogramme(request):
    return render(request,"imgprocess/egalisation_histogramme.html",{})


def basic_operation(request):
    return render(request,"imgprocess/image_operation.html")


def convolution(request):
    return render(request,"imgprocess/convolution.html")

def author(request):
    return render(request,"about.html")

def interpolation(request):
    return render(request,"imgprocess/interpolation.html")

def median_filter(request):
    return render(request,"imgprocess/median_filter.html")
