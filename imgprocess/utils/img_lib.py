import numpy as np
import os
from PIL import Image
class ImgLib:
    def __init__(self):
        pass
    
    @classmethod
    def get_normalize_vector(cls,img_matrix):
        h=[0 for i in range(256)]
        nb_pixel=img_matrix.shape[0]*img_matrix.shape[1]
        #calculons lhistogramme
        range_j=range(img_matrix.shape[1])
        for i in range(img_matrix.shape[0]):
            for j in range_j:
                h[img_matrix[i][j]]+=1
        h_normalize=[elt/nb_pixel for elt in h]
        #normalisation of probality density
        c_normalize=[]
        new_image=np.zeros(img_matrix.shape,dtype=int)
        #Calcul des densite de probabablite
        #for i in range(len(h_normalize)):
        #    c_i=0.0
        #    for j in range(i):
        #        c_i+=h_normalize[j]
        #    c_normalize.append(c_i)
        c_normalize=np.cumsum(h_normalize)
        #print("la sum est",c_normalize)
        #print(c_normalize)
        return {"c":c_normalize,"h":h}
    
    @classmethod
    def get_image_matrix(cls,img_file):
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
                i=0
                for element in data:
                    if(element[0]!="#" and element!=""):
                        final_data.append(element)
                        i+=1
                dimmension=final_data[1].split(" ")
                final_data.pop(0)
                final_data.pop(0)
                final_data.pop(i-3)
                final_matrix=np.reshape([int(elt) for elt in final_data],(int(dimmension[0]),int(dimmension[1])))
        
        return final_matrix
    
    @classmethod
    def _normalize_pixel(cls,img_matrix,pixel_value):
        """private funtion to calulate the normalize of some pixel"""
        
        h=list(range(0,256))
        nb_pixel=img_matrix.shape[0]*img_matrix.shape[1]
        h_normalize=[elt/nb_pixel for elt in h]
        normalize_pixel=0
        for i in range(pixel_value):
            normalize_pixel+=h_normalize[i]
        return normalize_pixel

    @classmethod
    def linea_transformation(cls,img_matrix,saturation_min=0,saturation_max=0):
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
        new_image=np.zeros(dimesnion,dtype="uint8")
        for i in range(dimesnion[0]):
            for j in range(dimesnion[1]):
                new_image[i][j]=int((255/differecence)*(img_matrix[i][j]-min_pixel))
                if new_image[i][j]<0:
                    new_image[i][j]=0
                elif new_image[i][j]>255:
                    new_image[i][j]=255
        
        return new_image
    
    @classmethod
    def linea_transformation_rgb(cls,img_matrix,saturation_min=0,saturation_max=0):
        """That function make linear tranformation on the image, it can make default 
        linear transformation or it can lake linear tranformation with saturation.
        
        If condition about saturation max and saturation min are not verify, algorithme will make 
        default linear tranformation"""
        max_pixel=saturation_max
        min_pixel=saturation_min
        #max_pixel=np.max(img_matrix)
        #min_pixel=np.min(img_matrix)
        #if(saturation_min>0 and saturation_max>0):
        #    if(min_pixel<=saturation_min and saturation_min<saturation_max and saturation_max<=max_pixel):
        #        max_pixel=saturation_max
        #        min_pixel=saturation_min

        difference=max_pixel-min_pixel
        pixel_len=len(img_matrix[0][0])
        range_pixel_len=range(pixel_len)
        range_column=range(img_matrix.shape[1])      
        for i in range(img_matrix.shape[0]):
            for j in range_column:
                for k in range_pixel_len:
                    img_matrix[i][j][k]=int((255/difference)*(img_matrix[i][j][k]-min_pixel))
        return img_matrix
    
    @classmethod
    def histogram_normalisation(cls,img_matrix):
        c_normalize=cls.get_normalize_vector(img_matrix)["c"]
        for i in range(img_matrix.shape[0]):
            for j in range(img_matrix.shape[1]):
                img_matrix[i][j]=int(c_normalize[img_matrix[i][j]]*255)
        
        return img_matrix
    
    @classmethod
    def histgramm_normalisation_rbg(cls,img_matrix):
        c_normalize=cls.get_normlize_vector(img_matrix)["c"]
        pixel_len=len(img_matrix[0][0])
        range_pixel_len=range(pixel_len)
        range_column=range(img_matrix.shape[1])
        for i in range(img_matrix.shape[0]):
            for j in range_column:
                for k in range_pixel_len:
                    img_matrix[i][j][k]=min(c_normalize[img_matrix[i][j][k]]*255,255)
        return img_matrix

    @classmethod
    def add_two_image(cls,img_matrix1,img_matrix2,mult_fact_1=1,mult_fact_2=1):
        """That function take two image matrix in parameter, supooe to be the same and 
        make the summ"""
        dimension=img_matrix1.shape
        new_matrix=np.zeros(dimension,dtype="uint8")
        for i in range(dimension[0]):
            for j in range(dimension[1]):
                pixel=img_matrix1[i][j]*mult_fact_1+img_matrix2[i][j]*mult_fact_2
                if(pixel>255):
                    pixel=255
                new_matrix[i][j]=pixel
        return new_matrix
    
    @classmethod
    def subtract_two_image(cls,img_matrix1,img_matrix2,mult_fact_1=1,mult_fact_2=1):
        """That function take two image matrix in parameter, supooe to be the same and 
        make the subtraction"""
        dimension=img_matrix1.shape
        new_matrix=np.zeros(dimension,dtype="uint8")
        for i in range(dimension[0]):
            for j in range(dimension[1]):
                pixel=img_matrix1[i][j]*mult_fact_1-img_matrix2[i][j]*mult_fact_2
                if(pixel<0):
                    pixel=0
                new_matrix[i][j]=pixel
        return new_matrix


    @classmethod
    def or_operation(cls,img_matrix1,img_matrix2):
        """Take to image matrix and make the or operation"""
        dimension=img_matrix1.shape
        new_matrix=np.zeros(dimension,dtype="uint8")
        for i in range(dimension[0]):
            for j in range(dimension[1]):
                new_matrix[i][j]=int(img_matrix1[i][j])|int(img_matrix2[i][j])
        return new_matrix
    
    @classmethod
    def and_operation(cls,img_matrix1,img_matrix2):
        """Take to image matrix and make the and operation"""
        dimension=img_matrix1.shape
        new_matrix=np.zeros(dimension,dtype="uint8")
        for i in range(dimension[0]):
            for j in range(dimension[1]):
                new_matrix[i][j]=int(img_matrix1[i][j]) & int(img_matrix2[i][j])
        return new_matrix

    @classmethod
    def convolution(cls,img_matrix,kernel):
        """That function take the matrix of image and convolution
        The principe of convolution is to make translation of convolution matrix
        on the img matrix, at each time, the center of submatrix take the sum of all  values multiplity
        of arround pixel with the convolution matrix
        @img_matrix must be an numpy array
        @kernel matrix must be an numpy array"""

        dimension=img_matrix.shape
        new_img_matrix=np.zeros(dimension)
        #We need to know were will be the center of convolution
        #now we will consider only 3*3 convolution matrix
        for i in range(0,dimension[0]-1):
            for j in range(0,dimension[1]-1):
                p_pixel=img_matrix[i-1][j-1]*kernel[0][0]+img_matrix[i-1,j]*kernel[0][1]+img_matrix[i-1,j+1]*kernel[0][2]+img_matrix[i,j-1]*kernel[1][0]+img_matrix[i][j]*kernel[1][1]+img_matrix[i][j+1]*kernel[1,2]+img_matrix[i+1][j-1]*kernel[2][0]+img_matrix[i+1][j]*kernel[2][1]+img_matrix[i+1,j+1]*kernel[2][2]
                new_img_matrix[i][j]=p_pixel
        return new_img_matrix
    
    @classmethod
    def convolution2(cls,img_matrix,kernel):
        """That function take the matrix of image and convolution
        The principe of convolution is to make translation of convolution matrix
        on the img matrix, at each time, the center of submatrix take the sum of all  values multiplity
        of arround pixel with the convolution matrix
        @img_matrix must be an numpy array
        @kernel matrix must be an numpy array"""

        #we take the center of the matrix
        center=int((kernel.shape[1]-1)/2)
        dimension=img_matrix.shape
        kernel_shape=kernel.shape
        new_img_matrix=np.zeros(img_matrix.shape,dtype="uint8")
        for i in range(center,dimension[0]-center):
            for j in range(center,dimension[1]-center):
                pixel_somme=0
                for u in range(kernel_shape[0]):
                    for v in range(kernel_shape[1]):
                        pixel_somme+=img_matrix[i-u-1][j-v-1]*kernel[u][v]
                pixel_somme=int(pixel_somme)
                if(pixel_somme<0):
                    pixel_somme=0
                elif(pixel_somme>255):
                    pixel_somme=0

                new_img_matrix[i][j]=pixel_somme
        return new_img_matrix
    
    @classmethod
    def basic_interpolation(cls,img_matrix,zoom_factor):
        """That function take matrix in parameter and the zoom-factor
        and make basic interpolation which consist to make a copy of pixel """
        zoom_factor=int(zoom_factor)
        dim=img_matrix.shape
        new_img_matrix=np.zeros((dim[0]*zoom_factor,dim[1]*zoom_factor),dtype=int)
        #creation de la matrice 
        sub_matrix=np.zeros((zoom_factor,zoom_factor),dtype=int)
        range_2=list(range(dim[1]))
        for i in list(range(dim[0])):
            for j in range_2:
                #nous devons creez une matrice donc la taille est 
                #zoom-facto*zoom_factor
                current_sub_matrix=np.full((zoom_factor,zoom_factor),img_matrix[i][j],dtype=int)
                new_img_matrix[i*zoom_factor:i*zoom_factor+zoom_factor,j*zoom_factor:j*zoom_factor+zoom_factor]=current_sub_matrix
        print(img_matrix[0,0])
        print(new_img_matrix[0:2,0:2])

        return new_img_matrix
    
    @classmethod
    def save_matrix_as_pgm(cls,img_matrix,name):
        data_to_write=""
        with open("imgprocess/static/imageprocess/images/"+name+".pgm","w+") as f:
            img_matrix_as_list=[str(elt) for elt in np.reshape(img_matrix,img_matrix.shape[0]*img_matrix.shape[1])]
           
            string_matrix=""
            string_matrix="\n".join(img_matrix_as_list)
            string_matrix="\n"+str(img_matrix.shape[0])+" "+str(img_matrix.shape[1])+"\n"+string_matrix
            string_matrix="P2"+"\n"+"#Create by the app img process make by Apache https://www.gihub.com/apachefranklin"+string_matrix+"\n"
           
            f.write(string_matrix)
            data_to_write=string_matrix
        with open("imgprocess/static/imageprocess/images/result/"+name+".pgm","w+") as f:
            f.write(data_to_write)

    @classmethod
    def median_filter(cls,img_matrix,voisinage):
        center=int(voisinage/2)
        dimension=img_matrix.shape
        new_img_matrix=np.zeros(img_matrix.shape,dtype=int)
        for i in range(center,dimension[0]-center):
            for j in range(center,dimension[1]-center):
                voisinnage=img_matrix[i-center:i+center+1,j-center:j+center+1]
                #print(voisinnage.shape)
                new_img_matrix[i][j]=np.median(np.reshape(voisinnage,voisinage*voisinage))
        return new_img_matrix




#img=[[34,56],[69,60]]
#img=np.array(img)
#print(np.max(img))