from django.db import models
from django.urls import reverse
    

class Meal(models.Model):
    breakfast = models.CharField(max_length=50)
    lunch = models.CharField(max_length=50)
    dinner = models.CharField(max_length=50)
    snacks = models.CharField(max_length=50)
    
    def __str__(self):
        return f'You had {self.breakfast} in the morning, {self.lunch} for lunch and {self.dinner} at night'
    
    def get_absolute_url(self):
        return reverse('meal_create')