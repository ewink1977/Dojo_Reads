from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields.related import ForeignKey
import re

class UsersManager(models.Manager):
    def basic_validation(self, postData):
        errors = {}
        if len(postData['name']) < 5:
            errors['name'] = 'Name needs to be at least 5 characters'
        if len(postData['alias']) < 5:
            errors['alias'] = 'Your alias needs to be at least 5 characters.'
        alias_dup_check = Users.objects.filter(alias = postData['alias'])
        if alias_dup_check == postData['alias']:
            errors['alias2'] = 'Your alias already exists. Alias needs to be unique.'
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):    # test whether a field matches the pattern            
            errors['email'] = 'Invalid email address!'
        emaildupcheck = Users.objects.filter(email=postData['email'])
        if emaildupcheck == postData['email']:
            errors['email2'] = 'That email address already exists. Did you forget your password?'
        if len(postData['password']) < 8:
            errors['password'] = 'Your password must be at least 8 characters long.'
        if not postData['confirm_password'] == postData['password']:
            errors['confirm_password'] = 'Password mismatch. Did you make a typo?'
        return errors

class Users(models.Model):
    name = models.CharField(max_length = 100)
    alias = models.CharField(max_length = 100)
    email = models.EmailField()
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UsersManager()

class AuthorsManager(models.Manager):
    def basic_validation(self, postData):
        errors = {}
        if postData['bookauthoradd']:
            if len(postData['bookauthoradd']) < 5:
                errors['author'] = 'Author name must be at least 5 characters long.'
        return errors

class Authors(models.Model):
    name = models.CharField(max_length = 100)
    created_by = models.DateTimeField(auto_now_add = True)
    updated_by = models.DateTimeField(auto_now = True)
    objects = AuthorsManager()

class BooksManager(models.Manager):
    def basic_validation(self, postData):
        errors = {}
        try:
            Books.objects.get(title = postData['booktitle'])
            errors['title'] = 'Book title already exists. If this is a different book with the same title, please add the year published to the end of the title (e.g. Babe (1999)).'
        except:
            pass
        if len(postData['booktitle']) < 5:
            errors['title'] = 'Title must be at least 5 characters long.'
        return errors

class Books(models.Model):
    title = models.CharField(max_length = 255)
    author = models.ForeignKey(
        Authors,
        related_name = "books",
        on_delete = CASCADE
    )
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = BooksManager()

class ReviewsManager(models.Manager):
    def basic_validation(self, postData):
        errors = {}
        if len(postData['bookreview']) < 10:
            errors['bookreview'] = 'Reviews must be at least 10 characters long.'
        if int(postData['bookrating']) < 1 or int(postData['bookrating']) > 5:
            errors['bookrating'] = 'Rating is required and it must be between 1 and 5 stars.'
        return errors

class Reviews(models.Model):
    review = models.TextField()
    rating = models.IntegerField()
    user = models.ForeignKey(
        Users,
        related_name = 'reviews',
        on_delete = CASCADE
    )
    book = models.ForeignKey(
        Books,
        related_name = 'reviews',
        on_delete = CASCADE
    )
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = ReviewsManager()