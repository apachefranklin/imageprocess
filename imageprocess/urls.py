
from django.contrib import admin
from django.urls import path,include
from imgprocess import views as imgviews

urlpatterns = [
    path("",imgviews.index,name="home"),
    path("process/",include("imgprocess.urls")),
    path('admin/', admin.site.urls),
]
