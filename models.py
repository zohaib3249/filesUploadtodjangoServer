from django.db import models
from rsca.models import *
fileStatus={
    ("Complete","Complete"),
    ("Incomplete","Incomplete"),
}
# Create your models here.
class FilesUpload(models.Model):
    filename=models.CharField(max_length=255)
    uploadUser=models.ForeignKey(Company_User,on_delete=models.CASCADE)
    TotalFileSize=models.BigIntegerField(default=0)
    status=models.CharField(choices=fileStatus,default="Incomplete",max_length=100)
    uploadedFileSize=models.BigIntegerField(default=0)
    dateTime=models.DateTimeField(default=timezone.now)
    offset=models.BigIntegerField(default=0)
    index=models.BigIntegerField(default=0)
    completed_at = models.DateTimeField(null=True,blank=True)

    

    def __str__(self):
        return self.filename

    def get_absolute_url(self):
        return reverse("FilesUpload_detail", kwargs={"pk": self.pk})
