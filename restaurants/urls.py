from django.urls import path

from restaurants.views import (
    CreateMenuView,
    CreateRestaurantView,
    ListMenuView,
    MenuVoteAPIView,
)

app_name = "restaurants"

urlpatterns = [
    path("create/", CreateRestaurantView.as_view(), name="create"),
    path("menus/", ListMenuView.as_view(), name="menus"),
    path("add-menu/", CreateMenuView.as_view(), name="add-menu"),
    path("menus/<int:menu_id>/vote/", MenuVoteAPIView.as_view(), name="vote"),
]
