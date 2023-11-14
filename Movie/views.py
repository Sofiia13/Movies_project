import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.http import HttpResponse
from datetime import datetime
from .forms import CreateUserForm
from django.contrib.auth.forms import UserCreationForm
from .models import Movie
from django.contrib.auth.decorators import login_required

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages


from django.http import JsonResponse
import random
import json


def registerPage(request):

    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)


            return redirect('login')

    context = {
        'form': form,
    }
    return render(request, 'register.html', context)

def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('show')



        else:
            messages.info(request, 'Username or password is incorrect')

    context = {}
    return render(request, 'login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


def list(request):
    user_id = request.user.id

    languages = {
        'en-US': 'English',
        'uk-UA': 'Ukrainian',
    }
    selected_language = request.POST.get('language')
    selected_language_code = selected_language
    if selected_language_code == 'uk-UA':
        watchlist_url = f"https://api.themoviedb.org/3/account/{user_id}/watchlist/movies?language=uk-UA"
        favorite_url = f"https://api.themoviedb.org/3/account/{user_id}/favorite/movies?language=uk-UA"
        popularity_url = f"https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=uk-UA&page=1&page=2&sort_by=popularity.desc"
        genres_url = f"https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=uk-UA&page=1&page=2&sort_by=popularity.desc&with_genres=Western%2C%20War%2C%20Thriller%2C%20TV%20Movie%2C%20Action%2C%20Adventure%2C%20Animation%2C%20Comedy%2C%20Crime%2C%20Documentary%2C%20Drama%2C%20Family%2C%20Fantasy%2C%20History%2C%20Horror%2C%20Music%2C%20Mystery%2C%20Romance%2C%20Science%20Fiction%2C%20Romance"
        all_genres_id_url = f"https://api.themoviedb.org/3/genre/movie/list?language=uk-UA"
    else:
        watchlist_url = f"https://api.themoviedb.org/3/account/{user_id}/watchlist/movies?language=en-US"
        favorite_url = f"https://api.themoviedb.org/3/account/{user_id}/favorite/movies?language=en-US"
        popularity_url = f"https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page=1&page=2&sort_by=popularity.desc"
        genres_url = f"https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page=1&page=2&sort_by=popularity.desc&with_genres=Western%2C%20War%2C%20Thriller%2C%20TV%20Movie%2C%20Action%2C%20Adventure%2C%20Animation%2C%20Comedy%2C%20Crime%2C%20Documentary%2C%20Drama%2C%20Family%2C%20Fantasy%2C%20History%2C%20Horror%2C%20Music%2C%20Mystery%2C%20Romance%2C%20Science%20Fiction%2C%20Romance"
        all_genres_id_url = f"https://api.themoviedb.org/3/genre/movie/list?language=en-US"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJjYjcyODE1ZDE2YzBjMmY5M2Y1YWJjMzJhNjlkNzE2YyIsInN1YiI6IjY1MmZiMjM5MzU4ZGE3NWI1ZDAwYTcxMyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.DkIixQiDr_Qb00rbzsDECmPGPfovi5uitXQad9O4EZ8"
    }

    response_popularity = requests.get(popularity_url, headers=headers)
    response_genres = requests.get(genres_url, headers=headers)
    response_all_genres_id = requests.get(all_genres_id_url, headers=headers)
    response_watchlist = requests.get(watchlist_url, headers=headers)
    response_favorite = requests.get(watchlist_url, headers=headers)
    movies_data = response_popularity.json()['results']
    genres_data = response_genres.json()['results']
    ids_data = response_all_genres_id.json()['genres']
    if response_watchlist.status_code == 200:
        watchlist_movies = response_watchlist.json().get('results')
    else:
        watchlist_movies = None
    if response_favorite.status_code == 200:
        favorite_movies = response_favorite.json().get('results')
    else:
        watchlist_movies = None
    movies = []
    action = []
    crime = []
    cartoons = []
    watchlist = []
    drama = []
    all_genres_id = []

    # for watch in watchlist_movies:
    #     date = datetime.strptime(watch['release_date'], "%Y-%m-%d")
    #     formatted_date = date.strftime("%d.%m.%Y")
    #     watchlist.append({'title': watch['title'], 'poster_path': watch['poster_path'],
    #                    'popularity': watch['popularity'], 'release_date': formatted_date,
    #                    'vote_average': watch['vote_average'], 'overview': watch['overview'], 'id': watch['id']})

    for movie_data in movies_data:
        date = datetime.strptime(movie_data['release_date'], "%Y-%m-%d")
        formatted_date = date.strftime("%d.%m.%Y")
        movies.append({'title': movie_data['title'], 'poster_path': movie_data['poster_path'],
                       'popularity': movie_data['popularity'], 'release_date': formatted_date,
                       'vote_average': movie_data['vote_average'], 'overview': movie_data['overview'], 'id': movie_data['id']})


    for genre_item in genres_data:
        date = datetime.strptime(genre_item['release_date'], "%Y-%m-%d")
        formatted_date = date.strftime("%d.%m.%Y")
        if 28 in genre_item['genre_ids']:
            action.append({'title': genre_item['title'], 'poster_path': genre_item['poster_path'],
                           'popularity': genre_item['popularity'], 'release_date': formatted_date,
                           'vote_average': genre_item['vote_average'], 'overview': genre_item['overview'],
                           'genres': genre_item['genre_ids'], 'id': genre_item['id']})

        if 80 in genre_item['genre_ids']:
            crime.append({'title': genre_item['title'], 'poster_path': genre_item['poster_path'],
                          'popularity': genre_item['popularity'], 'release_date': formatted_date,
                          'vote_average': genre_item['vote_average'], 'overview': genre_item['overview'],
                          'genres': genre_item['genre_ids'], 'id': genre_item['id']})

        if 16 in genre_item['genre_ids']:
            cartoons.append({'title': genre_item['title'], 'poster_path': genre_item['poster_path'],
                             'popularity': genre_item['popularity'], 'release_date': formatted_date,
                             'vote_average': genre_item['vote_average'], 'overview': genre_item['overview'],
                             'genres': genre_item['genre_ids'], 'id': genre_item['id']})

        if 18 in genre_item['genre_ids']:
            drama.append({'title': genre_item['title'], 'poster_path': genre_item['poster_path'],
                          'popularity': genre_item['popularity'], 'release_date': formatted_date,
                          'vote_average': genre_item['vote_average'], 'overview': genre_item['overview'],
                          'genres': genre_item['genre_ids'], 'id': genre_item['id']})

    if selected_language_code == 'uk-UA':
        movies_with_title = {'items': movies, 'title': 'Популярні'}
        action_with_title = {'items': action, 'title': 'Бойовик'}
        crime_with_title = {'items': crime, 'title': 'Кримінал'}
        cartoons_with_title = {'items': cartoons, 'title': 'Мультики'}
        drama_with_title = {'items': drama, 'title': 'Драма'}
    else:
        movies_with_title = {'items': movies, 'title': 'Popular'}
        action_with_title = {'items': action, 'title': 'Action'}
        crime_with_title = {'items': crime, 'title': 'Crime'}
        cartoons_with_title = {'items': cartoons, 'title': 'Cartoons'}
        drama_with_title = {'items': drama, 'title': 'Drama'}

    context = {
        'languages': languages,
        'selected_language_code': selected_language_code,
        'movies': movies,
        'action': action,
        'all_genres_id': all_genres_id,
        'crime': crime,
        'cartoons': cartoons,
        'drama': drama,
        'watchlist_movies': watchlist_movies,
        'favorite_movies': favorite_movies,
        'carousels': [movies_with_title, action_with_title, crime_with_title, cartoons_with_title, drama_with_title],
        'userId': user_id,
        # 'watchlist': watchlist_with_title
    }

    return render(request, 'show.html', context)

def search(request):
    languages = {
        'en-US': 'English',
        'uk-UA': 'Ukrainian',
        # Add other languages as needed
    }
    selected_language = request.POST.get('language')
    selected_language_code = selected_language
    query = request.GET.get('query', '')
    api_key = 'cb72815d16c0c2f93f5abc32a69d716c'

    url = f'https://api.themoviedb.org/3/search/movie?query={query}&api_key={api_key}&language={selected_language_code}'

    response = requests.get(url)

    if response.status_code == 200:
        films_data = response.json()['results']
        films = []
        for film_data in films_data:
            date = datetime.strptime(film_data['release_date'], "%Y-%m-%d")
            formatted_date = date.strftime("%d.%m.%Y")
            films.append({'title': film_data['title'], 'poster_path': film_data['poster_path'],
                           'popularity': film_data['popularity'], 'release_date': formatted_date,
                           'vote_average': film_data['vote_average'], 'overview': film_data['overview'], 'id': film_data['id']})
        context = {
            'films': films,
            'query': query,
            'languages': languages,
            'selected_language_code': selected_language_code,
        }

        return render(request, 'search.html', context)


def add_to_watchlist(request, movie_id):
    # Log or print to verify the received movie ID
    print(f"Received movie ID: {movie_id}")

    # Construct the TMDb API URL
    url = f"https://api.themoviedb.org/3/account/{request.user.id}/watchlist"

    # Prepare the data to be sent in the POST request
    data = {
        "media_type": "movie",
        "media_id": movie_id,
        "watchlist": True
    }

    # Set the API key in the headers
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJjYjcyODE1ZDE2YzBjMmY5M2Y1YWJjMzJhNjlkNzE2YyIsInN1YiI6IjY1MmZiMjM5MzU4ZGE3NWI1ZDAwYTcxMyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.DkIixQiDr_Qb00rbzsDECmPGPfovi5uitXQad9O4EZ8",
    }

    # Send the POST request to add the movie to the watchlist
    response = requests.post(url, headers=headers, json=data)

    # Log the response content for debugging
    print(f"Response from TMDb API: {response.content}")

    if response.status_code == 201:
        return JsonResponse({"message": "Added to watchlist"})
    else:
        return JsonResponse({"message": "Failed to add to watchlist"}, status=400)

def remove_from_watchlist(request, movieId):
    # Log or print to verify the received movie ID
    print(f"Received movie ID: {movieId}")

    # Construct the TMDb API URL
    url = f"https://api.themoviedb.org/3/account/{request.user.id}/watchlist"

    # Prepare the data to be sent in the POST request
    data = {
        "media_type": "movie",
        "media_id": movieId,
        "watchlist": True
    }

    # Set the API key in the headers
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJjYjcyODE1ZDE2YzBjMmY5M2Y1YWJjMzJhNjlkNzE2YyIsInN1YiI6IjY1MmZiMjM5MzU4ZGE3NWI1ZDAwYTcxMyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.DkIixQiDr_Qb00rbzsDECmPGPfovi5uitXQad9O4EZ8",
    }

    # Send the POST request to add the movie to the watchlist
    response = requests.post(url, headers=headers, json=data)

    # Log the response content for debugging
    print(f"Response from TMDb API: {response.content}")

    if response.status_code == 201:

        return JsonResponse({"message": "Removed from watchlist"})
    else:
        return JsonResponse({"message": "Failed to remove from watchlist"}, status=400)


# def add_to_user_list(request, movie_id):
#     if request.method == 'POST':
#         movie = get_object_or_404(Movie, pk=movie_id)
#         # Here, you'll add the movie to the user's list
#         # This is a simplified example; replace this with your logic to add the movie to the user's list
#         # For example, if you have a UserList model, you might do something like: UserList.objects.create(user=request.user, movie=movie)
#         return JsonResponse({'message': 'Added to list'})  # Send a JSON response or customize as needed
