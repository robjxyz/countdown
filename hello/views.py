import urllib.request
import datetime, os
from django.shortcuts import render
from django.http import HttpResponse
from hello.gtfs_realtime_pb2 import *
from hello.nyct_subway_pb2 import *

from .models import Greeting

NYCT-API = os.environ['NYCT-API']

# Create your views here.
def index(request):
    feed = FeedMessage()
    gtfs_raw_Adiv = urllib.request.urlopen("http://datamine.mta.info/mta_esi.php?key="+NYCT-API+"&feed_id=1").read()
    gtfs_raw_NQRW = urllib.request.urlopen("http://datamine.mta.info/mta_esi.php?key="+NYCT-API+"&feed_id=16").read()
    gtfs_raw_ACE = urllib.request.urlopen("http://datamine.mta.info/mta_esi.php?key="+NYCT-API+"&feed_id=26").read()
    gtfs_raw_BDFM = urllib.request.urlopen("http://datamine.mta.info/mta_esi.php?key="+NYCT-API+"&feed_id=21").read()
    feed.ParseFromString(gtfs_raw_Adiv)
    def prettyTime(t):
        if '-' in t: return '0 min'
        h,m,s = t.split(':')
        h = int(h)
        m = int(m)
        s = int(s)
        if s>30: m += 1
        m += 60*h
        return '{0} min'.format(m)
    epkwy = []
    one145 = []
    for entity in feed.entity:
        if entity.trip_update.trip.route_id in ('2','3','4','5'):
            for stop_time_update in entity.trip_update.stop_time_update:
                if stop_time_update.stop_id == '238N':
                    #print str(stop_time_update.arrival)[6:-1]
                    epkwy.append((str(entity.trip_update.trip.route_id),str(datetime.datetime.fromtimestamp(int(str(stop_time_update.arrival)[6:-1]))-datetime.datetime.now()).split('.')[0]))
        if entity.trip_update.trip.route_id == '1':
            for stop_time_update in entity.trip_update.stop_time_update:
                if stop_time_update.stop_id == '114S':
                    one145.append((str(entity.trip_update.trip.route_id),str(datetime.datetime.fromtimestamp(int(str(stop_time_update.arrival)[6:-1]))-datetime.datetime.now()).split('.')[0]))
    epkwy.sort(key=lambda tup: tup[1])
    one145.sort(key=lambda tup: tup[1])
    context = {'epkwy':[]}
    context['one145']=[]
    for arrival in epkwy:
        context['epkwy'].append( '({0}) {1}'.format(arrival[0],prettyTime(arrival[1])))
    for arrival in one145:
        context['one145'].append( '({0}) {1}'.format(arrival[0],prettyTime(arrival[1])))    

    #now do it for NWRQ for 7av
    feed.ParseFromString(gtfs_raw_NQRW)
    seventh = []
    for entity in feed.entity:
        if entity.trip_update.trip.route_id in ('Q'):
            for stop_time_update in entity.trip_update.stop_time_update:
                if stop_time_update.stop_id == 'D25N':
                    #print str(stop_time_update.arrival)[6:-1]
                    seventh.append((str(entity.trip_update.trip.route_id),str(datetime.datetime.fromtimestamp(int(str(stop_time_update.arrival)[6:-1]))-datetime.datetime.now()).split('.')[0]))
    seventh.sort(key=lambda tup: tup[1])
    context['seventh']=[]
    for arrival in seventh:
        context['seventh'].append( '({0}) {1}'.format(arrival[0],prettyTime(arrival[1])))

#now do it for ABCD for 145th
    feed.ParseFromString(gtfs_raw_ACE)
    ad145 = []
    for entity in feed.entity:
        if entity.trip_update.trip.route_id in ('A','C'):
            for stop_time_update in entity.trip_update.stop_time_update:
                if stop_time_update.stop_id == 'A12S':
                    ad145.append((str(entity.trip_update.trip.route_id),str(datetime.datetime.fromtimestamp(int(str(stop_time_update.arrival)[6:-1]))-datetime.datetime.now()).split('.')[0]))
    feed.ParseFromString(gtfs_raw_BDFM)
    for entity in feed.entity:
        if entity.trip_update.trip.route_id in ('D','B'):
            for stop_time_update in entity.trip_update.stop_time_update:
                if stop_time_update.stop_id == 'D13S':
                    ad145.append((str(entity.trip_update.trip.route_id),str(datetime.datetime.fromtimestamp(int(str(stop_time_update.arrival)[6:-1]))-datetime.datetime.now()).split('.')[0]))
    
    ad145.sort(key=lambda tup: tup[1])
    context['ad145']=[]
    for arrival in ad145:
        context['ad145'].append( '({0}) {1}'.format(arrival[0],prettyTime(arrival[1])))

    
    return render(request, 'index.html',context)


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})

