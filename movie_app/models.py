from django.db import models
from datetime import date


class Category(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    url = models.SlugField(max_length=150, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"


class Actor(models.Model):
    name = models.CharField(max_length=50)
    age = models.PositiveSmallIntegerField(default=0)
    description = models.TextField()
    image = models.ImageField(upload_to="actors/")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Актори та режисери"
        verbose_name_plural = "Актори та режисери"


class Genre(models.Model):
    name = models.CharField(max_length=70)
    description = models.TextField()
    url = models.SlugField(max_length=150, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанри"


class Movie(models.Model):
    title = models.CharField(max_length=100)
    tagline = models.CharField(max_length=100, default='')
    description = models.TextField()
    poster = models.ImageField(upload_to="movies/")
    year = models.PositiveSmallIntegerField(default=2022)
    country = models.CharField(max_length=50)
    directors = models.ManyToManyField(Actor, related_name="film_director")
    actors = models.ManyToManyField(Actor, related_name="film_actor")
    genre = models.ManyToManyField(Genre)
    world_premiere = models.DateField(default=date.today)
    budget = models.PositiveIntegerField(default=0)
    fees_in_world = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    url = models.SlugField(max_length=150, unique=True)
    draft = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Фільм"
        verbose_name_plural = "Фільми"


class MovieShots(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to="movie_shots")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Кадр з фільму"
        verbose_name_plural = "Кадри з фільму"


class RatingStar(models.Model):
    value = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.value

    class Meta:
        verbose_name = "Зірка"
        verbose_name_plural = "Зірки"


class Rating(models.Model):
    ip = models.CharField(max_length=15)
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.star} - {self.movie}"

    class Meta:
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинги"


class Reviews(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=100)
    text = models.TextField(max_length=10000)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.movie}"

    class Meta:
        verbose_name = "Відгук"
        verbose_name_plural = "Відгуки"
