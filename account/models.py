from django.db import models
from django.conf import settings

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True,null=True)
    phone_number = models.CharField(max_length=20,blank=False)
    city = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    photo = models.ImageField(upload_to='user/%Y/%m/%d/',blank=True)

    def __str__(self):
        return f'Profile of {self.user.username}'