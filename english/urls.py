from django.urls import path
from .views import (
    HomeView, PublishWordBooksListView, TypingWordsView, WordBooksListView, WordsListView,
    delete_word, delete_wordbook, update_wordbook_publish
)

app_name = 'english'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('wordbooks/', WordBooksListView.as_view(), name='wordbooks'),
    path('update_wordbook_publish/', update_wordbook_publish, name='update_wordbook_publish'),
    path('words/<int:pk>', WordsListView.as_view(), name='words'),
    path('typing/<int:pk>', TypingWordsView.as_view(), name='typing'),
    path('publish_wordbooks/', PublishWordBooksListView.as_view(), name='publish_wordbooks'),
    path('delete_wordbook/<int:pk>', delete_wordbook, name='delete_wordbook'),
    path('delete_word/<int:pk>_<int:wordbook_id>', delete_word, name='delete_word'),
]