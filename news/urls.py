from django.urls import path, re_path
from . import views
from .views import NewsView, AllNewsView, CreateNewsView, redirect_to_all_news
from django.conf import settings
from pathlib import Path
from .utils import read_json

PROJECT_ROOT = Path(settings.BASE_DIR)

urlpatterns = [
    # path('', views.index, name='index'),
    path('', redirect_to_all_news, name="redirect_to_all_news_view"),
    path('news/', AllNewsView.as_view(), name='all_news_view'),
    path('news/create/', CreateNewsView.as_view(), name='create'),
    path('news/<int:link>/', NewsView.as_view(), name='news'),
    path('news/<str:link>/', NewsView.as_view(), name='news'),
]
