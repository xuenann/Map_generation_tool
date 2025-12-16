from django.urls import path
from . import views,tomap

urlpatterns = [
    path('', views.index, name='index'),
    path('upload_file', views.upload_file, name='upload_file'),
    path('upload_folder', views.upload_folder, name='upload_folder'),
    path('submit_input', views.submit_input, name='submit_input'),
    path('generate_map', views.generate_map, name='generate_map'),
]
