from django.urls import path
from . import  views, img_api

app_name="imageprocess"

urlpatterns=[
    path("home",views.index,name="home"),
    path("about",views.author,name="about"),
    path("constrate",views.constraste,name="constraste"),
    path("performconstrate",img_api._constrate,name="pluminecance"),

    path("egalisation",views.egalisation_histogramme,name="egalisation"),
    path("pegalisation",img_api._egalisation_histogramme,name="pegalisation"),
    path("two_image_operation",views.basic_operation,name="operation"),
    path("poperation",img_api._make_operation,name="poperation"),
    path("convolution",views.convolution,name="convolution"),
    path("pconvolution",img_api._convolution,name="pconvolution"),

    path("interpolation",views.interpolation,name="interpolation"),
    path("pinterpolation",img_api._interpolation,name="pinterpolation"),
    path("download",views.download_file,name="download"),
    path("median_filter",views.median_filter,name="median"),
    path("pmedian_filter",img_api._median_filter,name="pmedian")
]