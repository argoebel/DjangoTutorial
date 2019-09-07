# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from bs4 import BeautifulSoup
from urllib.request import urlopen as uReq

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


        my_url = 'https://www.allmusic.com/search/artists/'

        artist_name = "drake"

        my_url+=artist_name

        uClient = uReq(my_url)
        page_html = uClient.read()
        uClient.close()

        #html parsing
        page_soup = BeautifulSoup(page_html, "html.parser")

        #grabs all products
        containers = page_soup.findAll("ul", {"class":"search-results"})

        #print("Newegg Video Cards\n")

        for container in containers:
            print(container)
            #brand = container.find("div", "item-info")
            #brand = brand.div.a.img["title"]
            #print(brand)
            #title_container = container.findAll("a", {"class":"item-title"})
            #print(title_container)
            #product_name = title_container[0].text
            #print(product_name)
            #shipping_container = container.findAll("li", {"class":"price-ship"})
            #print(shipping_container)
            #shipping = shipping_container[0].text.strip()
            #print(shipping)
            #print()

            # counter_object = Counter.objects.get(pk=1)
            # counter_object.count += 1
            # counter_object.save()
            return redirect('homepage')
