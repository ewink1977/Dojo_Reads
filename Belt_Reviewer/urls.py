from django.urls import path
from . import views
	
urlpatterns = [
		path('', views.home, name = 'home'),
        path('register/', views.register_new_user, name = 'register'),
        path('login/', views.login, name = 'login'),
        path('logout/', views.logout, name = 'logout'),
        path('books/', views.book_reviews, name = 'book_reviews'),
        path('books/add_book/', views.add_book_review, name = 'add_book_review'),
        path('books/add_book/process', views.process_new_book_review, name = 'proc_new_book'),
        path('books/<bookid>/', views.view_book, name = 'view_book'),
        path('books/<bookid>/addreview', views.review_existing_book, name = 'review_book'),
        path('books/<reviewid>/confirm_delete', views.confirm_delete, name = 'confirm_delete_review'),
        path('books/<reviewid>/delete', views.delete_review, name = 'delete_review'),
        path('user/<userid>/', views.view_profile, name = 'user_profile'),
	]
