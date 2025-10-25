from datetime import date

from django.conf import settings
from django.db import models


class Dish(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=5, decimal_places=2)


class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Menu(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    dishes = models.ManyToManyField(Dish)
    date = models.DateField(default=date.today)

    class Meta:
        unique_together = ("restaurant", "date")


class MenuVote(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    menu = models.ForeignKey(
        Menu,
        on_delete=models.CASCADE,
        related_name="votes",
    )

    class Meta:
        unique_together = ("user", "menu")
