from django.http import JsonResponse
from django.shortcuts import render
from django.http import HttpResponseRedirect

import os
from .form import UploadFileForm
from .utils.img_lib import ImgLib
from .utils.utility import *
from PIL import Image
import numpy as np
from matplotlib import pyplot as plt

img_path="imgprocess/static/imageprocess/images/"
hist_path=img_path+"hist/"
hist_path_result=img_path+"histresult/"
result_path=img_path+"result/"

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
    """At the end we need to send the preview histogramme, the new histgramme
    and the final image"""
    image_info=save_image(request.FILES["imguploaded"],None)
    
    #we get the name of the preview_histogramme
    preview_his_name=get_random_string(20)+image_info["extension"];
    plt.hist(image_info["list"]);

    plt.savefig(hist_path+preview_his_name)
    plt.close()

   
    image_info["preview_hist"]=preview_his_name

    #we call function of equalisation on the matrix of image
    egalisation_his_matrix=ImgLib().histogram_normalisation(image_info["matrix"])
    #we get now the new image 

    print(egalisation_his_matrix)

    new_image=Image.fromarray(egalisation_his_matrix.astype(np.uint8))
    new_image_name=get_random_string(18)+image_info["extension"]
    new_image.save(result_path+new_image_name)

    #now we reshape our egalisation_his_matirx at the list and we create the plot
    new_image_as_list=egalisation_his_matrix.ravel()
    new_his_name=get_random_string(24)+image_info["extension"]
    plt.plot(new_image_as_list)
    plt.savefig(hist_path_result+new_his_name);
    plt.close()
    image_info["new_hist"]=new_his_name
    image_info["saved_name"]=new_image_name
    image_info["matrix"]=None
    
    return JsonResponse(image_info)


#api for make addifiton of image
def _make_operation(request):
    image_info_1=save_image(request.FILES["imgone"],None)
    image_info_2=save_image(request.FILES["imgtwo"],None)
    reshapes_matrix=get_same_matrix(image_info_1["matrix"],image_info_2["matrix"])
    mult_fact_1=float(request.POST.get("factor_one",1))
    mult_fact_2=float(request.POST.get("factor_two",1))
    #print(reshapes_matrix["matrix1"].shape)
    #print(reshapes_matrix["matrix2"].shape)
    #print("before")
    #print(image_info_1["matrix"].shape)
    #print(image_info_2["matrix"].shape)
    operation=request.POST["operation"]
    matrix1=reshapes_matrix["matrix1"]
    matrix2=reshapes_matrix["matrix2"]
    if(operation=="add"):
        new_img_matrix=ImgLib().add_two_image(matrix1,matrix2,mult_fact_1,mult_fact_2)
    elif(operation=="or"):
        new_img_matrix=ImgLib().or_operation(matrix1,matrix2)
    elif(operation=="and"):
        new_img_matrix=ImgLib().and_operation(matrix1,matrix2)
    else:
        new_img_matrix=ImgLib().subtract_two_image(reshapes_matrix["matrix1"],reshapes_matrix["matrix2"],mult_fact_1,mult_fact_2)
    
    new_img_matrix=new_img_matrix.astype(np.uint8)
    new_img=Image.fromarray(new_img_matrix)

    new_image_name=get_random_string(random.randint(15,20))+image_info_1["extension"]
    new_img.save(result_path+new_image_name)

    image_info_1["matrix"]=None
    image_info_1["saved_name"]=new_image_name
    return JsonResponse(image_info_1)


def _convolution(request):
    """take all data come from convolution page and make all operation
    about convolution, now we consider only the 3*3 convolution matrix"""
    conv_field=request.POST["convolution_matrix"]
    conv_field=conv_field.split("\r\n")
    conv_matrix=np.zeros((3,3))
    for i in range(len(conv_field)):
        elts=conv_field[i].split()
        elts=[float(elt) for elt in elts]
        conv_matrix[i,]=elts
    image_info=save_image(request.FILES["imguploaded"],img_path)
    new_img_matrix=ImgLib().convolution(image_info["matrix"],conv_matrix)

    new_img_matrix=new_img_matrix.astype(np.uint8)
    new_img=Image.fromarray(new_img_matrix)

    new_image_name=get_random_string(random.randint(15,20))+image_info["extension"]
    new_img.save(img_path+new_image_name)

    image_info["matrix"]=None
    image_info["saved_name"]=new_image_name
    return JsonResponse(image_info)