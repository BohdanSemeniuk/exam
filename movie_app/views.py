from django.shortcuts import render
from django.views import View
from .models import Movie, Genre
from .serializers import MovieSerializer, GenreSerializer
from rest_framework import generics, decorators

#
# class GenreListCreate(generics.ListCreateAPIView):
#     queryset = Genre.objects.all()
#     serializer_class = GenreSerializer


class MovieView(View):
    def get(self, request):
        movies = Movie.objects.all()
        return render(request, 'movie_app/base.html', {'movie_list': movies})
