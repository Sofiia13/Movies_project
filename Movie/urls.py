from django.urls import path
from . import views


urlpatterns = [
    # path("", views.home, name = 'home'),
    #path("data/", views.get_data_from_api, name="data")
    path("show/", views.list, name='list'),
    path("search/", views.search, name='search'),

]