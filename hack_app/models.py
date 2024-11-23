from django.db import models

class image_model(models.Model):
    image = models.ImageField(null = True,blank = True, upload_to = "images/")
    

class classes(models.Model):
    cat = models.TextField()
# Create your models here.

class Response(models.Model):
    image_id = models.CharField(max_length=100)
    x1 = models.IntegerField()
    x2 = models.IntegerField()
    y1 = models.IntegerField()
    y2 = models.IntegerField()

