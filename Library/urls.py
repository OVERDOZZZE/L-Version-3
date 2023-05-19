from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from .views import *

urlpatterns = [
    path("", all_books, name='all_books'),
    path("detail_book/<int:id>/", book_info, name='book_detail'),
    path("detail_book/<int:id>/update/", alter_book, name='update_book'),
    path("add_book/", new_book),
    path("add_author/", new_author),
    path("add_publisher/", new_publisher),
    path('login/', login_func, name='login')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
