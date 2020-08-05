from django.shortcuts import render
from urllib.parse import quote_plus

from googleapiclient.discovery import build
#from apiclient.discovery import build

from bs4 import BeautifulSoup
import requests

from .models import Search

BASE_YOUTUBE_URL = 'https://www.googleapis.com/youtube/v3/search'

DEVELOPER_KEY = "AIzaSyCKQ2GlHh4ki7nz1iaXJ4_jiXbXML76qFk"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def home(request):
    return render(request, 'base.html')

def new_search(request):
    search = request.POST.get('search')
    #Search.objects.create(search=search)

    youtube = build(
        YOUTUBE_API_SERVICE_NAME,
        YOUTUBE_API_VERSION,
        developerKey=DEVELOPER_KEY
    )

    search_response = youtube.search().list(
        q=quote_plus(search),
        part="snippet",
        type="video",
        maxResults=30
    ).execute()

    print(search_response)
    print("-------------------------------------------------------------------------------")
    posts = []

    for search_result in search_response.get("items", []):
        if search_result["kind"] == "youtube#searchResult":
            print("--------------------In If---------------------------------")
            post_url = "https://www.youtube.com/watch?v=" + search_result["id"]["videoId"]
            post_image = search_result["snippet"]["thumbnails"]["high"]["url"]
            post_title = search_result["snippet"]["title"]
            post_description = search_result["snippet"]["description"]
            post_account = search_result["snippet"]["channelTitle"]

            print((post_url, post_image, post_title, post_description, post_account))
            print("--------------------")
            posts.append((post_url, post_image, post_title, post_description, post_account))



    context = {
        'search': search,
        'posts':posts
    }

    return render(request, 'my_app/new_search.html', context)








  # videos = []
  # channels = []
  # playlists = []


  # for search_result in search_response.get("items", []):
  #   if search_result["id"]["kind"] == "youtube#video":
  #     videos.append("%s (%s)" % (search_result["snippet"]["title"],
  #                                search_result["id"]["videoId"]))
  #   elif search_result["id"]["kind"] == "youtube#channel":
  #     channels.append("%s (%s)" % (search_result["snippet"]["title"],
  #                                  search_result["id"]["channelId"]))
  #   elif search_result["id"]["kind"] == "youtube#playlist":
  #     playlists.append("%s (%s)" % (search_result["snippet"]["title"],
  #                                   search_result["id"]["playlistId"]))

