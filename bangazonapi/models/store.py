from django.db import models
from .customer import Customer


class Store(models.Model):
    seller = models.ForeignKey(
        Customer, on_delete=models.DO_NOTHING, related_name="stores"
    )
    name = models.CharField(max_length=55)
    description = models.CharField(max_length=155)
    created_date = models.DateField(auto_now_add=True)


    @property
    def is_favorite(self):           
        return self.__is_favorite

    @is_favorite.setter
    def is_favorite(self, value):
        self.__is_favorite = value