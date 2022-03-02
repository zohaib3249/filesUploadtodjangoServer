from api.models import FilesUpload
from rest_framework import serializers
from rsca.models import *
class userSerailizers(serializers.ModelSerializer):
    class Meta:
        model = Company_User
        fields = '__all__'
class fileSerailizers(serializers.ModelSerializer):
    class Meta:
        model=FilesUpload
        fields='__all__'