import string
import random
from PIL import Image
from .img_lib import ImgLib
import os
import numpy as np
import random,math


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
    saved_name=get_random_string(random.randint(15,20))+file_extension
    saved_path="imgprocess/static/imageprocess/images/"+saved_name
    handle_uploaded_file(image_file,saved_path)
    
    imgglib=ImgLib()
    file_extension=str(file_extension).lower()
    type_elt="int"
    if(file_extension!=".pgm"):
        img_final=Image.open("imgprocess/static/imageprocess/images/"+saved_name)
        img_data=img_final.getdata()
        print(type(img_data))
        img_list_data=list(img_data)
        #print(img_final.size)
        #print(len(img_list_data))
        test_elemen=img_list_data[0]
        type_elt=type(test_elemen)
        img_matrix=np.zeros(img_final.size,dtype=object)
        if(type_elt is int):
            type_elt="int"
            img_matrix=np.reshape(img_list_data,img_final.size)
        elif(type_elt is tuple):
            type_elt="tuple"
            img_list_data2=[list(elt) for elt in img_list_data]
            img_matrix=np.array((img_final.size[0],img_final.size[1],3),dtype="uint8")
            min_indice=0
            max_indice=img_final.size[1]
            for i in range(img_final.size[0]):
                img_matrix[i,]=np.array(img_list_data2[min_indice:max_indice],dtype="uint8")
                min_indice=max_indice
                max_indice=max_indice+img_final.size[1]
            
    else:
       img_matrix= ImgLib.get_image_matrix(saved_path)
       img_list_data=img_matrix.ravel()

    print("elet type",type_elt)
    print("shape:", img_matrix.shape)
    #print("size: ",img_final.size)
    print("First element: ",img_matrix[0][0])
    print(img_matrix[0][0])

    return {"matrix":img_matrix,
            "path":"imgprocess/static/imageprocess/images/"+saved_name,
            "name":saved_name,
            "list":img_list_data,
            "extension":file_extension,
            "type":type_elt}


def get_same_matrix(matrix1,matrix2):
    """The goal of this function is to take two matrix
    and return the difference between col row of each matrix, to determine
    which matrix will be comple by zeros matrix in their column or rows"""
    shape1=matrix1.shape
    shape2=matrix2.shape

    diff_col=shape1[1]-shape2[1]
    diff_row=shape1[0]-shape2[0]
    
    result={"more_big":0,"more_col":0,
    "more_row":0,"diff_col":0,
    "diff_row":0}
    result["diff_col"]=int(math.fabs(diff_col))
    result["diff_row"]=int(math.fabs(diff_row))
    if(diff_col<0):
        result["more_col"]=2
        #add diff col on matrix one
        news_cols=np.zeros((shape1[0],result["diff_col"]))
        matrix1=np.concatenate((matrix1,news_cols),axis=1)
    elif(diff_col>0):
        result["more_col"]=1
        news_cols=np.zeros((shape2[0],result["diff_col"]))
        matrix2=np.concatenate((matrix2,news_cols),axis=1)
    if(diff_row<0):
        result["more_row"]=2
        #add diff row on matrix one
        news_rows=np.zeros((result["diff_row"],matrix1.shape[1]))
        matrix1=np.concatenate((matrix1,news_rows),axis=0)
    elif(diff_row>0):
        result["more_row"]=1
        news_rows=np.zeros((result["diff_row"],matrix2.shape[1]),dtype=int)
        matrix2=np.concatenate((matrix2,news_rows),axis=0)
    
    result["matrix1"]=matrix1
    result["matrix2"]=matrix2

    return result


