#!/usr/bin/python
# -*- coding: utf8 -*-


#CACHE_URL="http://webcache.googleusercontent.com/search?q=cache:"
CACHE_URL=""

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import settings

from django.db import models
from video.models import Movie

from xgoogle.browser import Browser
from xgoogle.BeautifulSoup import *

import sys, datetime

from os.path import dirname, abspath

from xgoogle.search import GoogleSearch, SearchError

def remove_html_tags(data):
    p = re.compile(r'<.*?>')
    return p.sub(' ', data)

def remove_extra_spaces(data):
    p = re.compile(r'\s+')
    return p.sub(' ', data)

def strip(data):
    return remove_html_tags( remove_extra_spaces( str(data) ) )

def update_from_web( model, film, year ):
  search = "kinopoisk.ru " + year + " " + film
  print "Search: %s" % search  
  browser=Browser(debug=True)
  gs = GoogleSearch(search)
  gs.results_per_page = 1
  results = gs.get_results()
  try:
    for res in results:
      pageurl = res.url.encode('utf8')
      page = browser.get_page( pageurl )
      soup = BeautifulStoneSoup( page[ page.find("<html"):], convertEntities=BeautifulStoneSoup.HTML_ENTITIES, fromEncoding="windows-1251" )
      print "URL: %s" % pageurl
      rating = soup.find('a',attrs={'class':'continue'})
      if rating:
	  r = strip(rating).split(' ')
          try:
              model.rating = float( r[1] )
              print "Rating: %s" % r[1] 
          except Exception, ex:
              model.rating = 0.0
              print "Can't parse rating"
 
      title = soup.find('h1','moviename-big')
      if title:
          print "Title: %s" % strip(title)
          model.title = strip(title)

      info = soup.find('span','_reachbanner_')
      if info:
          print "Info: %s" % strip(info)
          model.description = strip( info )

      img = soup.find('img', attrs={"width" : "120"})
      if img:
          print "Image: %s" % img['src']
	  model.image = "http://www.kinopoisk.ru%s" % img['src']
   
#getTrailer("t26538","397494/kinopoisk.ru-District-9-36971.mp4","397494/1_36971.jpg","480","270","tr","","");

      import re
      m = re.search("getTrailer\((.*)\)",str(soup))
      if not m:
          pass
      else:
          parts = m.group(1).split('"')
          url = "http://tr.kinopoisk.ru/%s" % parts[3]
	  model.trailer = url
	  image = "http://tr.kinopoisk.ru/%s" % parts[5]
          model.trailer_image = image
          print "Trailer: %s" % url
          print "TrailerImage: %s" % image
     
      break
  
  except Exception,e:
      print "WARNING: %s" % e

  finally:
      pass

for line in open( sys.argv[1] ):
  (year,film,rufilm) = line.decode('utf-8').split(';')
  movie = Movie()
  movie.year = int( year )
  movie.title = film
  movie.typeid = "movie"
  movie.owner_id = 1
  movie.publish = datetime.datetime.now()
  movie.unpublish = datetime.datetime.now()
  movie.price = 1.0
  movie.views = 0

  update_from_web( movie, rufilm , year )

  movie.save()


