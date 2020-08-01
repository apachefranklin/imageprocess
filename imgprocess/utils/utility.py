import string
import random

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