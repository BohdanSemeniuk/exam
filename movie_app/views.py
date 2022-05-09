from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth import models, decorators, authenticate, login
from django.contrib import messages
from django.views.generic import ListView, DetailView, TemplateView
from googleapiclient.discovery import build

from movie_site.settings import API_KEY
from .models import Movie, Genre
from .forms import ReviewForm
# import requests


class Home(TemplateView):
    template_name = 'movie_app/index.html'


class Data:
    def get_years(self):
        return Movie.objects.filter(draft=False).values("year").distinct().order_by('year')

    def get_genres(self):
        return Genre.objects.all()


@method_decorator(decorators.login_required, name='dispatch')
class MovieView(ListView, Data):
    model = Movie
    queryset = Movie.objects.filter(draft=False)
    template_name = 'movie_app/movie_list.html'
    paginate_by = 8


@method_decorator(decorators.login_required, name='dispatch')
class MovieDetailView(DetailView):
    model = Movie
    slug_field = 'url'
    template_name = 'movie_app/movie_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        movie_name = context['movie'].get_absolute_url().replace('/', '').replace('_', ' ')

        # context['video'] = self._get_video_id(movie_name)
        context['form'] = ReviewForm()
        return context

    def _get_video_id(self, title):
        you = build('youtube', 'v3', developerKey=API_KEY)

        request = you.search().list(
            part='snippet',
            maxResults=1,
            q=title + ' trailer'
        )
        video = request.execute()['items'][0]['id']['videoId']
        # video = requests.get(request.uri).json()['items'][0]['id']['videoId']
        return video


class Register(TemplateView):
    template_name = 'movie_app/register.html'

    def post(self, request):
        if request.method == 'POST':
            username = request.POST['username']
            email = request.POST['email']
            password1 = request.POST['password1']
            password2 = request.POST['password2']

            if password1 != password2:
                messages.error(request, '⚠️ Паролі не збігаються! Спробуйте ще раз')
                return redirect('register')

            if models.User.objects.filter(username=username).exists():
                messages.error(request, '⚠️ Ім`я користувача вже існує!')
                return redirect('register')

            if models.User.objects.filter(email=email).exists():
                messages.error(request, '⚠️ Адреса електронної пошти вже існує!')
                return redirect('register')

            user = models.User.objects.create_user(username=username, email=email)
            user.set_password(password1)
            user.save()

            messages.success(request, '✅ Реєстрація успішна!')
            return redirect('register')


class Login(TemplateView):
    template_name = 'movie_app/login.html'

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if not models.User.objects.filter(username=username).exists():
            messages.error(request, '⚠️ Ім`я користувача не існує!')
            return redirect('login')

        if user is None:
            messages.error(request, '⚠️ Ім`я користувача не існує!!')
            return redirect('login')

        if user is not None:
            login(request, user)
            return redirect(reverse('movie_list'))


class AddReview(View):
    def post(self, request, pk):
        form = ReviewForm(request.POST)
        movie = Movie.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get('parent', None):
                form.parent_id = int(request.POST.get('parent'))
            form.movie = movie
            form.name = request.user.username
            form.email = request.user.email
            form.save()
        return redirect(movie.get_absolute_url())


class Search(ListView, Data):
    paginate_by = 4

    def get_queryset(self):
        return Movie.objects.filter(title__iregex=self.request.GET.get("search"))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['q'] = f'search={self.request.GET.get("search")}&'
        return context


class FilterMovie(ListView, Data):
    paginate_by = 8

    def get_queryset(self):
        queryset = Movie.objects.filter(draft=False)
        if 'year' in self.request.GET:
            queryset = queryset.filter(year__in=self.request.GET.getlist('year'))
        if 'genre' in self.request.GET:
            queryset = queryset.filter(genre__in=self.request.GET.getlist('genre'))
        return queryset.distinct()
