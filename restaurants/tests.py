from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from restaurants.models import Dish, Menu, Restaurant
from users.models import User


class RestaurantMenuTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )
        self.client.force_authenticate(user=self.user)
        self.restaurant = Restaurant.objects.create(
            name="Pizzeria",
            address="Street 1",
        )
        self.menu_create_url = reverse("restaurants:add-menu")

    def test_create_menu(self):
        payload = {
            "restaurant": self.restaurant.id,
            "dishes": [
                {"name": "Margherita Pizza", "price": "8.50"},
                {"name": "Caesar Salad", "price": "6.00"},
            ],
        }
        res = self.client.post(self.menu_create_url, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data["restaurant"], self.restaurant.id)
        self.assertEqual(len(res.data["dishes"]), 2)

    def test_vote_menu(self):
        menu = Menu.objects.create(restaurant=self.restaurant)
        pizza = Dish.objects.create(name="Margherita Pizza", price=8.5)
        menu.dishes.add(pizza)
        vote_url = reverse("restaurants:vote", args=[menu.id])

        res = self.client.post(vote_url)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data["status"], "voted")
        self.assertEqual(menu.votes.count(), 1)

        res = self.client.post(vote_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["status"], "already voted")
        self.assertEqual(menu.votes.count(), 1)
