from django.urls    import path
from products.models import Category

from products.views import (
    CategoryView,
    MenuView,
    ProductView
)

urlpatterns = [
    path('/menus',                               MenuView.as_view()),
    path('/categories',                          CategoryView.as_view()),
    path('/menus/<str:menu_name>',               CategoryView.as_view()),
    path('',                                     ProductView.as_view()),
    path('/<str:menu_name>/<str:category_name>', ProductView.as_view())
]