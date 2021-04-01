from django.shortcuts import render, redirect, HttpResponse
import bcrypt
from django.contrib import messages
from .models import *

def index(request):
    return render(request, 'index.html')

def user_id(request, user_id):
    context = {
        "one_user": User.objects.get(id=user_id)
    }
    return render( request, "index.html", context)

def create_user(request):
    if request.method == "POST":
        errors = User.objects.create_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            password = request.POST['password']
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=pw_hash)
            request.session['user_id'] = user.id
            return redirect('/books')
    return redirect('/')

def display_books(request):
    if "user_id" not in request.session:
        return redirect('/')
    context = {
        "current_user": User.objects.get(id=request.session['user_id']),
        "all_books": Book.objects.all()
    }
    return render(request, "main_page.html", context)

def login(request):
    if request.method == "POST":
        user_with_email = User.objects.filter(email=request.POST['email'])
        if user_with_email:
            user = user_with_email[0]
            if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
                request.session['user_id'] = user.id
                return redirect('/books')
        messages.error(request,"Email or Password is incorrect")
    return redirect('/')

def logout(request):
    request.session.flush()
    return redirect('/')

def add_book(request):
    if "user_id" not in request.session:
        return redirect('/')
    if request.method == "POST":
        errors = Book.objects.book_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/books')
        else:
            current_user = User.objects.get(id=request.session['user_id'])
            adding_book = Book.objects.create(title = request.POST['book_title'], desc = request.POST['book_desc'], uploaded_by = current_user)
            # this_fav_book = Book.objects.get(id=book_id)
            current_user = User.objects.get(id=request.session['user_id'])
            adding_book.liked_by.add(current_user)
            print(current_user.first_name)
            return redirect('/books')
    return redirect('/books')


def one_book(request, book_id):
    if "user_id" not in request.session:
        return redirect('/')
    current_user = User.objects.get(id=request.session['user_id'])
    context = {
        "current_user": User.objects.get(id=request.session['user_id']),
        "current_book": Book.objects.get(id=book_id),
        "all_user":  Book.objects.get(id=book_id).liked_by.all(),
        "user_who_like":  Book.objects.get(id=book_id).liked_by
    }
    print (Book.objects.first().liked_by)
    return render(request, "one_book.html", context)

def book_update(request, book_id):
    if "user_id" not in request.session:
        return redirect('/')
    book_to_update = Book.objects.get(id=book_id)
    book_to_update.desc = request.POST['this_book_desc']
    book_to_update.title = request.POST['book_title']
    book_to_update.save()
    messages.success(request, "Your book has been updated!")
    return redirect(f'/books/{book_id}')

def book_delete(request, book_id):
    if "user_id" not in request.session:
        return redirect('/')
    book_to_delete = Book.objects.get(id=book_id)
    book_to_delete.delete()
    return redirect('/books')

def fav_book(request, book_id):
    if "user_id" not in request.session:
        return redirect('/')
    this_fav_book = Book.objects.get(id=book_id)
    current_user = User.objects.get(id=request.session['user_id'])
    this_fav_book.liked_by.add(current_user)
    print('--------------')
    return redirect('/books')

def unfav_book(request, book_id):
    if "user_id" not in request.session:
        return redirect('/')
    this_fav_book = Book.objects.get(id=book_id)
    current_user = User.objects.get(id=request.session['user_id'])
    this_fav_book.liked_by.remove(current_user)
    return redirect('/books')