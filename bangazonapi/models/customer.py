from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):

    user = models.OneToOneField(User, on_delete=models.DO_NOTHING,)
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=55)

    @property
    def recommends(self):           
        return self.__recommends

    @recommends.setter
    def recommends(self, value):
        self.__recommends = value

    @property
    def recommended_by(self):
        return self.__recommended_by
    
    @recommended_by.setter
    def recommended_by(self, value):
        self.__recommended_by = value
