
from django.contrib import admin
from django.urls import path,include
from improcess import views as imgviews

urlpatterns = [
    path("",imgviews.index,name="home"),
    path("process/",include("imageprocess.urls")),
    path('admin/', admin.site.urls),
]
