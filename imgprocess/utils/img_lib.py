import numpy as np
import os
from PIL import Image
class ImgLib:
    def __init__(self):
        pass
    
    def get_image_matrix(self,img_file):
        """That function take an image file and return matrix of image
        We use Image class of PIL library and numpy librairies to tranform hour image into matrix of 
        pixel"""
        file_name,file_extension=os.path.splitext(str(img_file))
        #firts we try to open image by considering we receive birany file
        final_matrix=[]
        try:
            image_file=Image.open(img_file)
            image_data=list(image_file.getdata())
            final_matrix=np.reshape(image_data,img_file.size)
        except:
            #sil ya erreur on essaye une ouverture normale
            #en considerent que nous sommes face a un fichier pgm bien 
            #ecrit
            with open(str(img_file),"r") as file:
                data=file.read()
                data=data.splitlines()
                final_data=[]
                for element in data:
                    if(element[0]!="#" and element!=""):
                        final_data.append(element)
                dimmension=final_data[1].split(" ")
                final_data.pop(0)
                final_data.pop(0)
                final_matrix=np.reshape([int(elt) for elt in final_data],(int(dimmension[0]),int(dimmension[1])))
        
        return final_matrix
    
    def _normalize_pixel(self,img_matrix,pixel_value):
        """private funtion to calulate the normalize of some pixel"""
        
        h=list(range(0,256))
        nb_pixel=img_matrix.shape[0]*img_matrix.shape[1]
        h_normalize=[elt/nb_pixel for elt in h]
        normalize_pixel=0
        for i in range(pixel_value):
            normalize_pixel+=h_normalize[i]
        return normalize_pixel

    def linea_transformation(self,img_matrix,saturation_min=0,saturation_max=0):
        """That function make linear tranformation on the image, it can make default 
        linear transformation or it can lake linear tranformation with saturation.
        
        If condition about saturation max and saturation min are not verify, algorithme will make 
        default linear tranformation"""

        max_pixel=np.max(img_matrix)
        min_pixel=np.min(img_matrix)
        if(saturation_min>0 and saturation_max>0):
            if(min_pixel<=saturation_min and saturation_min<saturation_max and saturation_max<=max_pixel):
                max_pixel=saturation_max
                min_pixel=saturation_min
        

        differecence=max_pixel-min_pixel
        lumine=np.mean(img_matrix)
        dimesnion=img_matrix.shape
        new_image=np.zeros(dimesnion,dtype=int)
        for i in range(dimesnion[0]):
            for j in range(dimesnion[1]):
                new_image[i][j]=int((255/differecence)*(img_matrix[i][j]-min_pixel))
                if new_image[i][j]<0:
                    new_image[i][j]=0
                elif new_image[i][j]>255:
                    new_image[i][j]=255
        
        return new_image
    
    def histogram_normalisation(self,img_matrix):
        h=list(range(1,256))
        nb_pixel=img_matrix.shape[0]*img_matrix.shape[1]
        h_normalize=[elt/nb_pixel for elt in h]
        #normalisation of probality density
        c_normalize=[[],[]]
        new_image=np.zeros(img_matrix.shape,dtype=int)
        for i in list(range(1,256)):
            c_normalize[i-1]=0
            for j in list(range(i)):
                pass
        
                




#img=[[34,56],[69,60]]
#img=np.array(img)
#print(np.max(img))