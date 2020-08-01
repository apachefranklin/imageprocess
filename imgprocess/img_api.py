from django.http import JsonResponse
from django.shortcuts import render
from django.http import HttpResponseRedirect

import os
from .form import UploadFileForm
from .utils.img_lib import ImgLib
from .utils.utility import *
from PIL import Image
import numpy as np

def _constrate(request):
    image_file=request.FILES["imguploaded"]
    #print(str(image_file))
    file_name,file_extension=os.path.splitext(str(image_file))
    saved_name=get_random_string(15)+file_extension
    #we save file to the disk
    handle_uploaded_file(request.FILES['imguploaded'],"imgprocess/static/imageprocess/images/"+saved_name)
    #file_name,file_extension="bonjour",".jpeg"
    imgglib=ImgLib()
    img_final=Image.open("imgprocess/static/imageprocess/images/"+saved_name)
    img_matrix=np.reshape(list(img_final.getdata()),img_final.size)
    #print(img_matrix.shape)
    #img_matrix=imgglib.get_image_matrix("imgprocess/static/imageprocess/images/"+saved_name)
    saturation_min=int(request.POST["saturation-min"])
    saturation_max=int(request.POST["saturation-max"])

    #appel de la tranformation lineaire
    final_matrix=imgglib.linea_transformation(img_matrix,saturation_min,saturation_max)
    #final_matrix=np.reshape(final_matrix,(final_matrix.shape[0]*final_matrix.shape[1]))
    img=Image.fromarray(final_matrix.astype(np.uint8))
    #maintenant nous devons creer un nom pour notre fichier
    
    img.save("imgprocess/static/imageprocess/images/result/"+saved_name)
    return JsonResponse({"original_name":str(image_file),"extention":file_extension,"saved_name":saved_name})

def _egalisation_histogramme(request):
    return JsonResponse({"status":True})