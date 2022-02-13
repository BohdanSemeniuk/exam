from rest_framework import serializers
from .models import *


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'url']


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ['id', 'name', 'age', 'description', 'image']


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('id', 'name', 'description', 'url')


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('id', 'title', 'tagline', 'description', 'poster', 'year', 'country',
                  'directors', 'actors', 'genre', 'world_premiere', 'budget',
                  'fees_in_world', 'category', 'url', 'draft')


class MovieShotsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieShots
        fields = ['id', 'title', 'description', 'image', 'movie']
