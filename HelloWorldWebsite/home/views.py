# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from bs4 import BeautifulSoup
from urllib.request import urlopen as uReq
from urllib.request import Request

from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse
from django.views import generic
from .models import Counter

# Create your views here.
class Home(generic.DetailView):
    model = Counter
    template_name = "home/index.html"

    def get(self, request, *args, **kwargs):
        context = {'our_counter' : Counter.objects.get(pk=1)}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        base_url = 'https://www.allmusic.com'
        search_url = 'https://www.allmusic.com/search/artists/'
        artist_name = "drake"
        search_url+=artist_name

        req = Request(search_url, headers={'User-Agent': 'Mozilla/5.0'})
        results_html = uReq(req).read()

        #html parsing
        page_soup = BeautifulSoup(results_html, "html.parser")

        #grabs all artists
        containers = page_soup.findAll("ul", {"class":"search-results"})
        artist_url = containers[0].div.a['href']
        print(artist_url)

        artist_img = containers[0].div.img['src']
        print(artist_img)

        related_url = base_url + artist_url + '/related'

        req = Request(related_url, headers={'User-Agent': 'Mozilla/5.0'})
        related_html = uReq(req).read()

        page_soup = BeautifulSoup(related_html, "html.parser")
        containers = page_soup.findAll("section", {"class":"related similars"})

        artist_list = []
        #print(containers)
        #print(len(containers))
        for container in containers:
            artist_return = container.findAll(text=True)

        for artist in artist_return:
            #print(str(artist))
            #print(type(str(artist)))
            artist_list.append(str(artist))

        fixed = []
        for artist in artist_list:
            if artist != '\n' and artist != ' ' and artist != "Similar To":
                fixed.append(artist)
        print(fixed)

        return redirect('homepage')
