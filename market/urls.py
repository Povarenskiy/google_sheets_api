from django.urls import path
from .views import OrderApiView

urlpatterns = [
    path('', OrderApiView.as_view()),
]
