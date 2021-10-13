from django.urls import path

from orders.views import CartView,CartEditView

urlpatterns = [
    path('/cart', CartView.as_view()),
    path('/cart/edit', CartEditView.as_view()),
]