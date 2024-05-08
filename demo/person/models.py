from django.db import models
from django.contrib.auth import get_user_model

User=get_user_model()
class Intro(models.Model):
    name=models.ForeignKey(User,on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.name}'
    

class ExpenseCategory(models.Model):
    itemname=models.CharField(null=False,max_length=20)

    def __str__(self):
        return f"{self.itemname}"
# Create your models here.
