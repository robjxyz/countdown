import urllib.request
import datetime, os
from django.shortcuts import render
from django.http import HttpResponse
from train_times.lib.gtfs_realtime_pb2 import *
from train_times.lib.nyct_subway_pb2 import *
from train_times.lookup import get_station_info, get_station_departures, valid

NYCTAPI = os.environ['NYCTAPI']

def prettyTime(t):
    if '-' in t: return '0 min'
    h,m,s = t.split(':')
    h = int(h)
    m = int(m)
    s = int(s)
    if s>30: m += 1
    m += 60*h
    return '{0} min'.format(m)

# Create your views here.
def index(request):
    feed = FeedMessage()
    gtfs_raw_Adiv = urllib.request.urlopen("http://datamine.mta.info/mta_esi.php?key="+NYCTAPI+"&feed_id=1").read()
    gtfs_raw_NQRW = urllib.request.urlopen("http://datamine.mta.info/mta_esi.php?key="+NYCTAPI+"&feed_id=16").read()
    gtfs_raw_ACE = urllib.request.urlopen("http://datamine.mta.info/mta_esi.php?key="+NYCTAPI+"&feed_id=26").read()
    gtfs_raw_BDFM = urllib.request.urlopen("http://datamine.mta.info/mta_esi.php?key="+NYCTAPI+"&feed_id=21").read()
    feed.ParseFromString(gtfs_raw_Adiv)

    epkwy = []
    one145 = []
    one148 = []
    for entity in feed.entity:
        if entity.trip_update.trip.route_id in ('2','3','4','5'):
            for stop_time_update in entity.trip_update.stop_time_update:
                if stop_time_update.stop_id == '238N':
                    epkwy.append((str(entity.trip_update.trip.route_id),str(datetime.datetime.fromtimestamp(int(str(stop_time_update.arrival)[6:-1]))-datetime.datetime.now()).split('.')[0]))
                elif stop_time_update.stop_id == '301N':
                    one148.append((str(entity.trip_update.trip.route_id),str(datetime.datetime.fromtimestamp(int(str(stop_time_update.arrival)[6:-1]))-datetime.datetime.now()).split('.')[0]))
    epkwy.sort(key=lambda tup: tup[1])
    one148.sort(key=lambda tup: tup[1])
    context = {'epkwy':[]}
    context['one145']=[]
    context['one148']=[]
    for arrival in epkwy:
        context['epkwy'].append( '({0}) {1}'.format(arrival[0],prettyTime(arrival[1])))
    for arrival in one145:
        context['one145'].append( '({0}) {1}'.format(arrival[0],prettyTime(arrival[1])))
    for arrival in one148:
        context['one148'].append( '({0}) {1}'.format(arrival[0],prettyTime(arrival[1])))

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

def one_stop_with_id(request, stop_id):
    if valid(stop_id):
        stop_name, direction = get_station_info(stop_id)
        departure_times = sorted(get_station_departures(stop_id), key=lambda d: d['time'])
        return render(request, 'one_stop.html', {'stop_name': stop_name,
                                                'direction': direction,
                                                'departure_times': departure_times})
    else:
        return render(request, 'invalid_stop.html')

def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})

