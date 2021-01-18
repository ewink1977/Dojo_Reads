from django.urls import path
from . import views
	
urlpatterns = [
		path('', views.home, name = 'home'),
        path('books/', views.book_reviews, name = 'book_reviews'),
        path('books/add_book/', views.add_book_review, name = 'add_book_review'),
	]
