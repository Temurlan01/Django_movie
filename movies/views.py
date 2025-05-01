from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.generic import View, ListView, DetailView
from .forms import ReviewForm
from .models import Movie, Category, Actor, Genre


class GenreYear:
    def get_genres(self):
        return Genre.objects.all()

    def get_years(self):
        return Movie.objects.filter(draft=False).values("year")


class MoviesView(GenreYear, ListView):
    model = Movie
    queryset = Movie.objects.filter(draft=False)
    template_name = "movies/movie.html"


class MovieDetailView(GenreYear, DetailView):
    model = Movie
    slug_field = "url"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["categories"] = Category.objects.all()
        return context


class AddReview( View):
    def post(self, request, pk):
        form = ReviewForm(request.POST)
        movie = Movie.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get("parent", None):
                form.parent_id = int(request.POST.get("parent"))
            form.movie = movie
            form.save()
        return redirect(movie.get_absolute_url())


class ActorView(GenreYear, DetailView):
    model = Actor
    template_name = 'movies/actor.html'
    slug_field = "name"


class FilterMoviesView(GenreYear, ListView):
    def get_queryset(self):
        if 'genre' in self.request.GET and 'year' in self.request.GET:
            print('if genre and year')
            queryset = Movie.objects.filter(
            Q(year__in=self.request.GET.getlist("year")) , Q(genres__in=self.request.GET.getlist("genre"))
        )
        else:
            print('else')
            queryset = Movie.objects.filter(
                Q(year__in=self.request.GET.getlist("year")) | Q(genres__in=self.request.GET.getlist("genre"))
            )
        return queryset
    template_name = "movies/movie.html"