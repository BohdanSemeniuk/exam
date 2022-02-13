from django.urls import path
from . import views


urlpatterns = [
    # path("api/genre/", views.GenreListCreate.as_view()),
    path("", views.MovieView.as_view()),
]
