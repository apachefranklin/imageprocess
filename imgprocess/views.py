from django.http import JsonResponse
from django.shortcuts import render
from django.http import HttpResponseRedirect

import os
from .form import UploadFileForm
from .utils.img_lib import ImgLib
from .utils.utility import *
from PIL import Image
import numpy as np
# Create your views here.


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