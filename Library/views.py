from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator
from django.http import HttpResponse

from django.shortcuts import render, redirect
from .models import Book, Author, Publisher
from .forms import AddPublisherForm, AddBookForm, AddAuthorForm


def all_books(request):
    book_list = Book.objects.all()
    paginator = Paginator(book_list, 5)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)
    context = {'books': page_object}

    return render(request, 'all_books.html', context=context)


def book_info(request, id):
    book = Book.objects.get(id=id)
    date = book.publication_date.strftime("%Y-%m-%d")
    authors = Author.objects.all()
    publishers = Publisher.objects.all()
    context = {'book': book,
               'authors': authors,
               'publishers': publishers,
               'date': date
               }
    return render(request, 'book_info.html', context=context)


def new_book(request):
    if request.method == 'POST':
        form = AddBookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('all_books')
    else:
        form = AddBookForm()
    return render(request, 'add_new.html', {'form': form})


def new_author(request):
    if request.method == 'POST':
        form = AddAuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('all_books')
    else:
        form = AddAuthorForm()
    return render(request, 'add_new.html', {'form': form})


def new_publisher(request):
    if request.method == 'POST':
        form = AddPublisherForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('all_books')
    else:
        form = AddPublisherForm()
    return render(request, 'add_new.html', {'form': form})


def login_func(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('all_books')
        else:
            return HttpResponse('Wrong password or login')

    return render(request, 'login.html')


def alter_book(request, id):
    book = Book.objects.get(id=id)

    if request.method == 'POST':
        book.title = request.POST.get('title')
        book.author = Author.objects.get(id=request.POST.get('author_id'))
        book.publisher = Publisher.objects.get(id=request.POST.get('publisher_id'))
        book.publication_date = request.POST.get('publication_date')
        if request.POST.get('cover_photo'):
            book.cover_photo = '{}{}'.format('media/', request.POST.get('cover_photo'))
        book.save()

    return redirect('book_detail', id=id)
