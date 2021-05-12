"""View module for handling requests about meals"""
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from django.http.response import Http404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from favamealapi.models import Meal, MealRating, Restaurant, FavoriteMeal
from favamealapi.views.restaurant import RestaurantSerializer
from django.contrib.auth.models import User


class MealSerializer(serializers.ModelSerializer):
    """JSON serializer for meals"""
    restaurant = RestaurantSerializer(many=False)

    class Meta:
        model = Meal
        # fields = ('id', 'name', 'restaurant', 'user_rating', 'avg_rating')
        fields = ('id', 'name', 'restaurant', 'favorite', 'rating', 'average_rating')

# class UserSerializer(serializers.ModelSerializer):
#     """JSON serializer for meal rater's related Django user"""
#     class Meta:
#         model = User
#         fields = ['first_name', 'last_name']

# class RatingSerializer(serializers.ModelSerializer):
#     """JSON serializer for MealRatings"""
#     meal = MealSerializer(many=False)
#     user = UserSerializer(many=False)

#     class Meta:
#         model = MealRating
#         fields = ['user', 'meal', 'rating']


class MealView(ViewSet):
    """ViewSet for handling meal requests"""

    def create(self, request):
        """Handle POST operations for meals

        Returns:
            Response -- JSON serialized meal instance
        """
        meal = Meal()
        meal.name = request.data["name"]
        meal.restaurant = Restaurant.objects.get(pk=request.data["restaurant_id"])


        try:
            meal.save()
            serializer = MealSerializer(
                meal, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single meal

        Returns:
            Response -- JSON serialized meal instance
        """
        user = User.objects.get(pk=request.auth.user.id)

        try:
            meal = Meal.objects.get(pk=pk)

            # TODO: Get the rating for current user and assign to `user_rating` property

            # TODO: Get the average rating for requested meal and assign to `avg_rating` property

            # TODO: Assign a value to the `is_favorite` property of requested meal
            try:
                FavoriteMeal.objects.get(meal=meal, user=user)
                meal.favorite = True
            except FavoriteMeal.DoesNotExist:
                meal.favorite = False

            try:
                ratingInstance = MealRating.objects.get(meal=meal, user=user)
                meal.rating = ratingInstance.rating
            except MealRating.DoesNotExist:
                meal.rating = 0


            serializer = MealSerializer(
                meal, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to meals resource

        Returns:
            Response -- JSON serialized list of meals
        """
        user = User.objects.get(pk=request.auth.user.id)
        
        meals = Meal.objects.all()

        # TODO: Get the rating for current user and assign to `user_rating` property

        # TODO: Get the average rating for each meal and assign to `avg_rating` property

        # TODO: Assign a value to the `is_favorite` property of each meal
        for meal in meals:
            try:
                FavoriteMeal.objects.get(meal=meal, user=user)
                meal.favorite = True
            except FavoriteMeal.DoesNotExist:
                meal.favorite = False
            
            try:
                ratingInstance = MealRating.objects.get(meal=meal, user=user)
                meal.rating = ratingInstance.rating
            except MealRating.DoesNotExist:
                meal.rating = 0
        

        serializer = MealSerializer(
            meals, many=True, context={'request': request})

        return Response(serializer.data)





    # TODO: Add a custom action named `star` that will allow a client to send a
    #  POST and a DELETE request to /meals/3/star.


    @action(methods=['post','delete'], detail=True)
    def star(self, request, pk=None):
        user = User.objects.get(pk=request.auth.user.id)

        try:
            meal = Meal.objects.get(pk=pk)
        except Meal.DoesNotExist:
            return Response(
                {'message': 'Meal not found in the database'},
                status=status.HTTP_404_NOT_FOUND
            )

        if request.method == "POST":
            try:
                meal.favorites.add(user)
                return Response({}, status=status.HTTP_201_CREATED)
            except Exception as ex:
                return Response({'message': ex.args[0]})

        elif request.method == "DELETE":
            try:
                meal.favorites.remove(user)
                return Response({}, status=status.HTTP_204_NO_CONTENT)
            except Exception as ex:
                return Response({'message': ex.args[0]})
    
    # TODO: Add a custom action named `rate` that will allow a client to send a
    #  POST and a PUT request to /meals/3/rate with a body of..
    #       {
    #           "rating": 3
    #       }
    @action(methods=['post','put'], detail=True)
    def rate(self, request, pk=None):
        user = User.objects.get(pk=request.auth.user.id)

        try:
            meal = Meal.objects.get(pk=pk)
        except Meal.DoesNotExist:
            return Response(
                {'message': 'Meal not found in the database'},
                status=status.HTTP_404_NOT_FOUND
            )

        if request.method == "POST":
            try:
                MealRating.objects.get(user=user, meal=meal)
                return Response(
                    {'message': 'You already rated this meal, use a PUT request!'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            except MealRating.DoesNotExist:
                rating = MealRating()
                rating.user = user
                rating.meal = meal
                rating.rating = request.data['rating']

                try:
                    rating.save()
                    return Response({}, status=status.HTTP_201_CREATED)
                except ValidationError as ex:
                    return Response({'reason': ex.message}, status=status.HTTP_400_BAD_REQUEST)
        
        if request.method == "PUT":
            try:
                rating = MealRating.objects.get(meal=meal, user=user)
            except MealRating.DoesNotExist:
                return Response({'message': 'You need to rate a meal before you can edit the rating'})

            rating.rating = request.data['rating']
            rating.save()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

