from django.conf.urls import url

from django.contrib import admin
from django.urls import path, include
from django.conf import  settings
from django.conf.urls.static import static


from api.views import *
urlpatterns = [
    
    path('Data_file/', Data_file),
    
    path('api-auth/', LoginUser),
    path('chunked_upload/', chunked_upload,name="chunked_upload"),
    path('fileUploadPut/', fileUploadPut,name="fileUploadPut"),
    
    
   
]

urlpatterns = urlpatterns+static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)