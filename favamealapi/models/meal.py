from favamealapi.models.mealrating import MealRating
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
    @property
    def rating(self):
        return self.__rating

    @rating.setter
    def rating(self, value):
        self.__rating = value

    # TODO: Add an avg_rating custom properties
    @property
    def average_rating(self):
        ratings = MealRating.objects.filter(meal=self)
        
        total_rating = 0
        for rating in ratings:
            total_rating += rating.rating

        average = 0
        if (len(ratings)):
            average = total_rating / len(ratings)
        return average