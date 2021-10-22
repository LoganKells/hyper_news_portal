import datetime
import random
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from django.shortcuts import render, redirect
from django.conf import settings
from pathlib import Path
from .utils import read_json, write_json

PROJECT_ROOT = Path(settings.BASE_DIR)
PATH_NEWS_JSON = PROJECT_ROOT / "hyper_news_portal" / "news.json"


def index(request):
    return HttpResponse(content="Coming soon.")


def redirect_to_all_news(request):
    return HttpResponseRedirect("news/")


def build_link_map(data: list) -> dict:
    # Build a dictionary of link keys to index in the news.json file list of data
    link_map = {}
    for i, news_data in enumerate(data):
        link = news_data["link"]
        link_map[link] = i
    return link_map


class NewsView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.news_data = read_json(path_to_json=PATH_NEWS_JSON)
        self.link_map = build_link_map(data=self.news_data)

    def get(self, request, *args, **kwargs):
        # Use the URL link key to identify the correct news to show, from NEWS_DATA hashmap.
        link = self.kwargs['link']  # Link is read dynamically from URL, see news.urls.py
        idx_news = self.link_map[link]
        news = self.news_data[idx_news]

        return render(request, "index.html", context=news)


class AllNewsView(View):
    # View all the news in hyper_news_portal/news.json
    def __init__(self, **kwargs):
        super(AllNewsView, self).__init__(**kwargs)
        self.news_data = read_json(path_to_json=PATH_NEWS_JSON)
        self.link_map = build_link_map(data=self.news_data)

    def get(self, request, *args, **kwargs):
        query = request.GET.get("q")
        if query is not None and int(query) in self.link_map.keys():
            idx = self.link_map[int(query)]
            response_data = {'news_data': [self.news_data[idx]]}
            # link = self.kwargs['link']  # Link is read dynamically from URL, see news.urls.py
            # idx_news = self.link_map[link]
            # news = self.news_data[idx_news]
            # return render(request, "index.html", context=news)
        else:
            response_data = {'news_data': self.news_data}
        return render(request, "main.html", context=response_data)


class CreateNewsView(View):
    def __init__(self, **kwargs):
        super(CreateNewsView, self).__init__(**kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, "create_news.html")

    def post(self, request, *args, **kwargs):
        # Read in the request data from the HTTP POST
        post_data = request.POST
        title, text = post_data["title"], post_data["text"]

        # Get today's date as a string
        now = datetime.datetime.now()
        now_str = str(now)

        # Generate a random link URL based on the current time
        link_timestamp = int(now.timestamp())

        # Build a news data in correct format for hyper_news_portal/news.json
        new_news_data = {"created": now_str, "text": text, "title": title, "link": link_timestamp}

        # Add the new news data to the existing data, and rewrite to the hyper_news_portal/news.json
        news_data = read_json(path_to_json=PATH_NEWS_JSON)
        news_data.append(new_news_data)
        write_json(path_to_json=PATH_NEWS_JSON, data=news_data)

        # After writing to the json, redirect to the news homepage
        return redirect("/news/")

