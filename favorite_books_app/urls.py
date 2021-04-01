from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.index),
    path('user/create', views.create_user),
    path('books', views.display_books),
    path('user/login', views.login),
    path('user/logout', views.logout),
    path('books/create', views.add_book),
    path('books/<int:book_id>', views.one_book),
    path('books/<int:book_id>/update', views.book_update),
    path('books/<int:book_id>/delete', views.book_delete),
    path('books/<int:book_id>/favorite', views.fav_book),
    path('books/<int:book_id>/unfavorite', views.unfav_book),
]