from django.urls import path
from . import views
	
urlpatterns = [
		path('', views.home, name = 'home'),
        path('books/', views.book_reviews, name = 'book_reviews'),
        path('books/add_book/', views.add_book_review, name = 'add_book_review'),
        path('books/ID/', views.view_book, name = 'view_book'),
        path('books/<bookid>/addreview', views.review_existing_book, name = 'review_book'),
        path('user/ID/', views.view_profile, name = 'user_profile'),
	]
