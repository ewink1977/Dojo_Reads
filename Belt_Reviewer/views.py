from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import Users, Authors, Books, Reviews
import bcrypt

# User Management

def home(request):
    context = {
        'page_title': 'DojoReads || Login or Register!'
    }
    return render(request, 'html/register_and_login.html', context)

def register_new_user(request):
    if request.method == 'POST':
        errors = Users.objects.basic_validation(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags='danger')
            return redirect('home')
        prehash_pw = request.POST['password']
        hashed_pw = bcrypt.hashpw(prehash_pw.encode(), bcrypt.gensalt()).decode()
        newuser = Users.objects.create(
            name = request.POST['name'],
            alias = request.POST['alias'],
            email = request.POST['email'],
            password = hashed_pw
        )
        print(f'USER NUMBER {newuser.id} CREATED.')
        request.session['userid'] = newuser.id
        request.session['loggedin'] = True
        messages.success(request, f"User { request.POST['alias'] } has been created successfully!")
        return redirect('book_reviews')
    else:
        messages.error(request, 'Invalid request. Please register or log in.', extra_tags = 'danger')
        return redirect('home')

def login(request):
    if request.method == 'POST':
        user = Users.objects.filter(email = request.POST['email'])
        if user:
            logging_in_user = user[0]
            if bcrypt.checkpw(
                request.POST['password'].encode(),
                logging_in_user.password.encode()
                ):
                request.session['userid'] = logging_in_user.id
                request.session['loggedin'] = True
                print(f'USER ID {logging_in_user.id} LOCATED, PASSWORD VERIFIED.')
                messages.success(request, f"Congrats! User {logging_in_user.alias} has logged in!")
                return redirect('book_reviews')
            else:
                messages.error(request, 'Unable to log in. The password you entered is incorrect.', extra_tags = 'danger')
                return redirect('home')
        else:
            messages.error(request, 'Unable to log in. The email you entered was not found in our system.', extra_tags = 'danger')
            return redirect('home')
    else:
        messages.error(request, 'Invalid request. Please register or log in.', extra_tags = 'danger')
        return redirect('home')

def logout(request):
    request.session.flush()
    request.session['loggedin'] = False
    return redirect('home')

# Book and Review VIEW Management

def book_reviews(request):
    if request.session['loggedin'] == True:
        context = {
            'page_title': 'Recent Book Reviews!',
            'current_user': Users.objects.get(id = request.session['userid']),
            'reviews': Reviews.objects.all().order_by("-created_at"),
        }
        return render(request, 'html/book_reviews.html', context)
    if request.session['loggedin'] == False:
        context = {
            'page_title': 'Recent Book Reviews!',
        }
        return render(request, 'html/book_reviews.html', context)

def add_book_review(request):
    if request.session['loggedin'] == False:
        messages.error(request, 'You must be logged in to add book reviews. Please log in!', extra_tags = 'danger')
        return redirect('home')
    else:
        context = {
            'page_title': 'Add A Book & Review!',
            'current_user': Users.objects.get(id = request.session['userid']),
            'authors': Authors.objects.all()
        }
        return render(request, 'html/new_book.html', context)

def view_book(request, bookid):
    book_info = Books.objects.get(id = bookid)
    context = {
        'page_title': f'{book_info.title} | Reviews!',
        'book_info': book_info,
        'user_info': Users.objects.get(id = request.session['userid'])
    }
    return render(request, 'html/view_reviews.html', context)

def view_profile(request):
    context = {
        'page_title': 'USER NAME | Profile!',
    }
    return render(request, 'html/user_profile.html', context)

def confirm_delete(request, reviewid):
    context = {
        'review_id': reviewid
    }
    return render(request, 'html/confirm_delete.html', context)

# Book and Review POST Management

def review_existing_book(request):
    if request.method == 'POST':
        review_errors = Reviews.objects.basic_validation(request.POST)
        if len(review_errors) > 0:
            for key, value in review_errors.items():
                messages.error(request, value, extra_tags='danger')
                return redirect('view_book', request.POST['bookid'])
        book_reviewed = Books.objects.get(id = request.POST['bookid'])
        user_reviewing = Users.objects.get(id = request.session['userid'])
        Reviews.objects.create(
            review = request.POST['bookreview'],
            rating = request.POST['bookrating'],
            user = user_reviewing,
            book = book_reviewed
        )
        messages.success(request, f"Woot! You have reviewed {book_reviewed.title}!")
        return redirect('view_book', request.POST['bookid'])
    else:
        messages.error(request, 'Invalid request. Returning you to the main page.', extra_tags = 'danger')
        return redirect('book_reviews')


def process_new_book_review(request):
    if request.method == 'POST':
        book_errors = Books.objects.basic_validation(request.POST)
        if len(book_errors) > 0:
            for key, value in book_errors.items():
                messages.error(request, value, extra_tags='danger')
        review_errors = Reviews.objects.basic_validation(request.POST)
        if len(review_errors) > 0:
            for key, value in review_errors.items():
                messages.error(request, value, extra_tags='danger')
        if request.POST['bookauthorselect'] == -1:
            if request.POST['bookauthoradd'] == '':
                messages.error(request, 'Doh! You need to either choose an author from the drop down, or add a new author!', extra_tags = 'danger')
            else:
                author_errors = Authors.objects.basic_validation(request.POST)
                if len(author_errors) > 0:
                    for key, value in author_errors.items():
                        messages.error(request, value, extra_tags='danger')
        if len(messages.get_messages(request)) > 0:
            return redirect('add_book_review')
        else:
            if request.POST['bookauthorselect'] == '-1':
                author = Authors.objects.create(
                    name = request.POST['bookauthoradd']
                )
            else:
                author = Authors.objects.get(id = request.POST['bookauthorselect'])
            user = Users.objects.get(id = request.session['userid'])
            book = Books.objects.create(
                title = request.POST['booktitle'],
                author = author
            )
            Reviews.objects.create(
                review = request.POST['bookreview'],
                rating = request.POST['bookrating'],
                user = user,
                book = book
            )
            messages.success(request, f"Woot! You have reviewed {book.title}!")
            bookid = book.id
            return redirect('view_book', bookid)
    else:
        messages.error(request, 'Invalid request. Returning you to the main page.', extra_tags = 'danger')
        return redirect('book_reviews')

def delete_review(request, reviewid):
    review_to_destroy = Reviews.objects.get(id = reviewid)
    review_to_destroy.delete()
    messages.success(request, 'Welp, that review has successfully sent to the ether. Ja ni.')
    return redirect('book_reviews')