# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from bs4 import BeautifulSoup
from urllib.request import urlopen as uReq
from urllib.request import Request
import unidecode

from django.shortcuts import render, redirect, reverse
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from .models import Counter, Artist

# Create your views here.
class Home(generic.DetailView):
    model = Counter
    template_name = "home/index.html"

    def get(self, request, *args, **kwargs):
        context = {'our_counter' : 1}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        base_url = 'https://www.allmusic.com'
        search_url = 'https://www.allmusic.com/search/artists/'
        artist_name = request.POST['input']
        artist_name = unidecode.unidecode(artist_name).replace(" ", "+")
        search_url+=artist_name

        req = Request(search_url, headers={'User-Agent': 'Mozilla/5.0'})
        results_html = uReq(req).read()

        #html parsing
        page_soup = BeautifulSoup(results_html, "html.parser")

        #grabs all artists
        containers = page_soup.findAll("ul", {"class":"search-results"})
        artist_url = containers[0].div.a['href']

        if artist_url[0:len(base_url)] == base_url:
            artist_url = artist_url[len('https://www.allmusic.com/artist/'):]
        print(artist_url)

        initial_artist_id = artist_url[-12:]

        if artist_url[0:7] != '/artist':
            artist_url = '/artist/'+artist_url

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

        try:
            Artist.objects.create(id=initial_artist_id, name=artist_name)
        except:
            print("Object Already Exists")

        Q = Artist.objects.get(pk=initial_artist_id)

        for artist in fixed[:10]:
            #adjusted_name = unicodedata.normalize("NFKD", unidecode.unidecode(artist)).replace(" ", "+")
            adjusted_name = unidecode.unidecode(artist).replace(" ", "+")

            #print(adjusted_name)

            search_url = 'https://www.allmusic.com/search/artists/' + adjusted_name
            #print(search_url)
            req = Request(search_url, headers={'User-Agent': 'Mozilla/5.0'})
            results_html = uReq(req).read()

            #html parsing
            page_soup = BeautifulSoup(results_html, "html.parser")

            containers = page_soup.findAll("ul", {"class":"search-results"})
            artist_url = containers[0].div.a['href']

            if artist_url[0:len(base_url)] == base_url:
                artist_url = artist_url[len('https://www.allmusic.com/artist/'):]

            artist_id = artist_url[-12:]
            #print(artist, " ", artist_id, " ")

            try:
                instance = Artist.objects.create(id=artist_id, name=artist)
            except:
                instance = Artist.objects.get(pk=artist_id)

            try:
                Q.related.add(instance)
            except:
                print("Object Already Exists")

        return render(request, "home/results.html", {
            'Artist': Q,
        })
