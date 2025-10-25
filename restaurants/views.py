from datetime import date

from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from restaurants.models import Menu, MenuVote
from restaurants.serializers import (
    MenuListSerializer,
    MenuSerializer,
    RestaurantSerializer,
)


class CreateRestaurantView(CreateAPIView):
    serializer_class = RestaurantSerializer


class CreateMenuView(CreateAPIView):
    serializer_class = MenuSerializer


class ListMenuView(ListAPIView):
    queryset = Menu.objects.filter(date=date.today())
    serializer_class = MenuListSerializer


class MenuVoteAPIView(APIView):
    def post(self, request, menu_id):
        try:
            menu = Menu.objects.get(id=menu_id)
        except Menu.DoesNotExist:
            return Response(
                {"detail": "Menu not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        vote, created = MenuVote.objects.get_or_create(
            menu=menu,
            user=request.user,
        )
        if created:
            return Response(
                {"status": "voted"},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {"status": "already voted"},
                status=status.HTTP_200_OK,
            )
