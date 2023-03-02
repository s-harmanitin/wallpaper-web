from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.

class tag(models.Model):
    title = models.CharField(max_length=40)
    
    def __str__(self):
        return self.title


class Post(models.Model):
    title = models.CharField(max_length=40,null=True)
    image = CloudinaryField('image')
    uploadby = models.CharField(max_length=40,null=True)
    tag = models.ForeignKey(tag,on_delete=models.CASCADE,null=True)
    desc = models.CharField(max_length=10000,null=True)
    likes = models.BigIntegerField(default=0)
    
    def __str__(self):
        return(self.title)
 
 
 
   
gender = (
    ('Male','Male'),
    ('Female','Female'),
    ('Others','Others'),
)
  
class userdetails(models.Model):
    name = models.CharField(max_length=40)
    phonenumber = models.BigIntegerField(default=0000000000)
    profileimage = CloudinaryField('image')
    gender = models.CharField(max_length=100,choices=gender,default='Male',null=True)
    
    def __str__(self):
        return(self.name)
    
    

class Like(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    post = models.ForeignKey(Post,on_delete=models.CASCADE,null=True)
    
    
    
    

    
    