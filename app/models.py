from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

# Create your models here.

account_type=(
   ( "individual","individual"),
    ("custodial","custodial")
)

investment_type=(
   ( "onetime","onetime"),
    ("recurring","recurring")
)

frequency=(
    ("none","none"),
   ( "monthly","monthly"),
    ("quaterly","quaterly")
)

class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    phone=models.CharField(max_length=50,blank=True,null=True)
    address=models.CharField(max_length=50,blank=True,null=True)
    state=models.CharField(max_length=50,blank=True,null=True)
    zip_code=models.CharField(null=True,blank=True,max_length=40)
    acct_type=models.CharField(max_length=50,blank=True,null=True,choices=account_type)
    social_number=models.CharField(max_length=50,blank=True,null=True)
    is_verified=models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} Profile '

class Investments(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    inv_type=models.CharField(max_length=50,blank=True,null=True,choices=investment_type)
    frequency_type=models.CharField(max_length=50,blank=True,null=True,choices=frequency)
    amount=models.IntegerField(null=True,blank=True)
    created=models.DateField(auto_now_add=True,null=True,blank=True)
    confirmed=models.BooleanField(default=False)
    image=CloudinaryField('image',blank=True,null=True)
    def __str__(self):
       return f'{self.user.first_name} {self.user.last_name} Investment '



