from django.urls import path
from . import  views, img_api

app_name="imageprocess"

urlpatterns=[
    path("home",views.index,name="home"),
    path("constrate",views.constraste,name="constraste"),
    path("performconstrate",img_api._constrate,name="pluminecance"),

    path("egalisation",views.egalisation_histogramme,name="egalisation"),
    path("pegalisation",img_api._egalisation_histogramme,name="pegalisation")
]