from api.models import FilesUpload
from rsca_website import settings
from django.http import response
from rsca.models import *
from django.http.response import  HttpResponse, JsonResponse

from rest_framework.decorators import api_view

from rest_framework.decorators import parser_classes
from rest_framework.parsers import *
from rest_framework.views import APIView
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os
from datetime import datetime
import io
from api.serializers import *
import cgi

@api_view(['POST'])
def LoginUser(request):
    if request.method=='POST':
        try:
            data=request.data    
            user=Company_User.objects.get(username=data["username"],password=data["password"])
            print(user)
            if user:
                ser=userSerailizers(user)
                return JsonResponse(ser.data,safe=False)
            else:
                return JsonResponse({'msg':"Username or Password invalid"},safe=False)
        except :
            return JsonResponse({'msg':"Error"},safe=False)
    else:
        return JsonResponse({"msg":"Get Request Method not allowed!!!"},safe=False)

@api_view(['POST'])
@parser_classes([FileUploadParser])
def Data_file(request):
    import re
    regex_http_          = re.compile(r'^HTTP_.+$')
    regex_content_type   = re.compile(r'^CONTENT_TYPE$')
    regex_content_length = re.compile(r'^Content-Disposition$')
    print("Zc")
    if request.method=="POST":
        
        file_obj = request.FILES['file']
        request_headers = {}


        for header in request.META:
            if regex_http_.match(header) or regex_content_type.match(header):
                request_headers[header] = request.META[header]
        
        
        _, params = cgi.parse_header(request_headers["HTTP_CONTENT_DISPOSITION"])
        print(params["filename"])
        print("re")
        """path = default_storage.save(params["filename"], ContentFile(file_obj.read()))
        tmp_file = os.path.join(settings.MEDIA_ROOT, path)
        f=open(tmp_file,"r")
        tx=f.read()"""
        return HttpResponse(params["filename"])

    else:
        print("Get Request")
        return HttpResponse("bad")
@api_view(['PUT'])

def fileUploadPut(request):
    if (request.method=="PUT"):
        data=request.data
        print(data)
        u=Company_User.objects.get(id=data["userid"])
        file,created=FilesUpload.objects.get_or_create(filename=data["filename"],
        uploadUser=u,TotalFileSize=data["TotalFileSize"]
        )
        if file.status=="complete":
            return JsonResponse("FIle already Uploaded")
        else:
            
            ser=fileSerailizers(file)
            return JsonResponse(ser.data,safe=False)
    else:
        return JsonResponse("Error",safe=False)
@api_view(['POST'])

def chunked_upload(request):

    if request.method=="POST":
        chunk = request.FILES['file'].read()
        file=FilesUpload.objects.get(id=request.POST['Fileid'])
        tempfile=open("stored_uploads/"+file.filename,'ab+')
        tempfile.write(chunk)
        tempfile.close()
        file.index=request.POST['offset']
        file.offset=request.POST['offset']
        file.save()
        if int(file.offset)>=int(file.TotalFileSize):
            file.status="Complete"
            file.completed_at=datetime.now()
            file.save()
        ser=fileSerailizers(file)
        return JsonResponse(ser.data,safe=False)       
    else:
        return JsonResponse("Error",safe=False)

    






