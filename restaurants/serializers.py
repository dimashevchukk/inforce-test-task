from rest_framework import serializers

from .models import Dish, Menu, MenuVote, Restaurant


class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = ["id", "name", "price"]


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ["id", "name", "address"]


class MenuSerializer(serializers.ModelSerializer):
    dishes = DishSerializer(many=True)

    class Meta:
        model = Menu
        fields = ["id", "restaurant", "date", "dishes"]

    def create(self, validated_data):
        dishes_data = validated_data.pop("dishes")
        menu = Menu.objects.create(**validated_data)
        for dish_data in dishes_data:
            dish, _ = Dish.objects.get_or_create(**dish_data)
            menu.dishes.add(dish)
        return menu


class MenuListSerializer(serializers.ModelSerializer):
    restaurant = RestaurantSerializer(read_only=True)
    dishes = DishSerializer(many=True)
    votes_count = serializers.IntegerField(
        source="votes.count",
        read_only=True,
    )

    class Meta:
        model = Menu
        fields = ["id", "restaurant", "dishes", "votes_count"]


class MenuVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuVote
        fields = ["id", "user", "menu"]

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)
