from django.urls import path
from . import views


urlpatterns = [
    # path("", views.home, name = 'home'),
    #path("data/", views.get_data_from_api, name="data")
    path("show/", views.list, name='show'),
    path("search/", views.search, name='search'),
    path("register/", views.registerPage, name='register'),
    path("login/", views.loginPage, name='login'),
    path("logout/", views.logoutUser, name='logout'),
    path('add_to_watchlist/<int:movie_id>', views.add_to_watchlist, name='add_to_watchlist'),
    path('remove_from_watchlist/<int:movieId>', views.remove_from_watchlist, name='remove_from_watchlist'),

]