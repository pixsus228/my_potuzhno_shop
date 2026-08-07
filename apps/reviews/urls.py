from django.urls import path
from .views import ReviewUpdateView

app_name = 'reviews'

urlpatterns = [
    path('<int:pk>/edit/', ReviewUpdateView.as_view(), name='review_edit'),
]
