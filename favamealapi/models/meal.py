from django.db import models
from django.contrib.auth.models import User


class Meal(models.Model):

    name = models.CharField(max_length=55)
    restaurant = models.ForeignKey("Restaurant", on_delete=models.CASCADE)
    favorites = models.ManyToManyField(User, through="favoritemeal")

    @property
    def favorite(self):
        return self.__favorite

    @favorite.setter
    def favorite(self, value):
        self.__favorite = value
        
    # TODO: Add an user_rating custom properties


    # TODO: Add an avg_rating custom properties
