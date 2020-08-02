import string
import random
from PIL import Image
from .img_lib import ImgLib
import os
import numpy as np


def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

# Imaginary function to handle an uploaded file.
def handle_uploaded_file(f,namepath_to_upload):
    with open(namepath_to_upload, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def move_upload_image(img_data,file_name):
     with open('imageprocess/static/imageprocess/images/'+file_name, 'wb+') as destination:
         destination.write(img_data)


def save_image(image_file,image_path):
    
    """ That function return the saved name, 
        the path and the matrix of image
    """
   
    file_name,file_extension=os.path.splitext(str(image_file))
    saved_name=get_random_string(15)+file_extension
    handle_uploaded_file(image_file,"imgprocess/static/imageprocess/images/"+saved_name)
    
    imgglib=ImgLib()

    img_final=Image.open("imgprocess/static/imageprocess/images/"+saved_name)

    img_list_data=list(img_final.getdata())

    img_matrix=np.reshape(img_list_data,img_final.size)

    return {"matrix":img_matrix,
            "path":"imgprocess/static/imageprocess/images/"+saved_name,
            "name":saved_name,
            "list":img_list_data,
            "extension":file_extension}

