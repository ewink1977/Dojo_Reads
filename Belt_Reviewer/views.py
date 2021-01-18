from django.shortcuts import render, redirect, HttpResponse

def home(request):
    context = {
        'page_title': 'DojoReads || Login or Register!'
    }
    return render(request, 'html/register_and_login.html', context)