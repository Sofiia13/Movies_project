from django.urls import path
from . import views

urlpatterns = [
    # path("", views.home, name = 'home'),
    #path("data/", views.get_data_from_api, name="data")
    path("show/", views.list, name='list'),
    # path("show/", views.action, name='action'),
    # path("show/", views.my_view, name='my_view'),
    # path("genre/", views.genres_list, name = 'genres_list'),

    # path('show/', views.show, name='show'),
]