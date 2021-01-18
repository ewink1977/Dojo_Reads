from django.shortcuts import render, redirect, HttpResponse

def home(request):
    context = {
        'page_title': 'DojoReads || Login or Register!'
    }
    return render(request, 'html/register_and_login.html', context)

def book_reviews(request):
    context = {
        'page_title': 'Recent Book Reviews!'
    }
    return render(request, 'html/book_reviews.html', context)

def add_book_review(request):
    context = {
        'page_title': 'Add A Book & Review!'
    }
    return render(request, 'html/new_book.html', context)

def view_book(request):
    context = {
        'page-title': 'BOOK TITLE | Reviews!'
    }
    return render(request, 'html/view_reviews.html', context)

def review_existing_book(request):
    pass