from django.urls import path

from users.views import SignUpView, SignInView

urlpatterns = [
    path('/cart', SignUpView.as_view()),
    path('/', SignInView.as_view()),
]