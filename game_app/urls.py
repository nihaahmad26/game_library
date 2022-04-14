from django.urls import path  
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin


from .views import *
from . import views



urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path("games", views.show_all),
    path("games/page", views.show_page),
    path("games/create", views.add_game),
    path("games/<int:game_id>/createreview", views.add_review),
    path("games/<int:game_id>/review", views.show_reviewpg),
    path("games/<int:game_id>", views.show_one),
    path("games/<int:game_id>/update", views.update),
    path("games/<int:game_id>/delete", views.delete),
    path("games/<int:game_id>/<int:review_id>/del", views.deletereview),
    path("games/<int:game_id>/<int:review_id>/upd", views.updatereview),
    path("games/<int:game_id>/<int:review_id>/updatereview", views.showupdatereview),
    path("/success", views.success),
    path('logout', views.logout)
] 



