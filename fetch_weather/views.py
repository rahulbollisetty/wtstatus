from django.shortcuts import render,redirect
import requests
import json
from .models import City
from .forms import CityForm
from django.contrib import messages
import datetime
from django.contrib.auth.models import User
from django.http import request
from django.contrib.auth.decorators import login_required
@login_required(login_url='login')
def index(request):
    url='http://api.openweathermap.org/data/2.5/forecast?q={}&appid=3f9ee007eef0401a6ae15ebd009a1b05&units=metric'
    cities = City.objects.filter(uname_id=request.user.id)#return all the cities in the database
    weather_data = []
    form = CityForm()
    # if request.method == 'POST': # only true if form is submitted
    #     form = CityForm(request.POST) # add actual request data to form for processing
    #     form.save() # will validate and save if validateform = CityForm()
    #     return redirect('weather')
    if request.method == 'POST':
        err_msg=''
        form = CityForm(request.POST)
        if form.is_valid():
            new_city = form.cleaned_data['name']
            existing_city_count = City.objects.filter(name=new_city).filter(uname_id=request.user.id).count()
            
            if existing_city_count == 0:
                r = requests.get(url.format(new_city)).json()
                if r['cod'] == "200":
                    f_form=form.save(commit=False)
                    f_form.uname=User.objects.get(pk=request.user.id)
                    form.save()
                else:
                    err_msg = 'City does not exist in the world!'
            else:
                err_msg = 'City already exists in the database!'

        if err_msg:
            redirect('weather')
            messages.warning(request,err_msg)
        else:
            redirect('weather')
            messages.success(request,"City Added Successfully")
    form = CityForm()
    data_list = []
    city_list=[]
    for city in cities:
        day = datetime.datetime.today()
        dt=day
        today_date = int(day.strftime('%Y%m%d'))
        forcast_data_list = {}
        city_weather = requests.get(url.format(city.name)).json() #request the API data and convert the JSON to Python data types
        for c in range(0, city_weather['cnt']):
            date_var1 = city_weather['list'][c]['dt_txt']
            date_time_obj1 = datetime.datetime.strptime(date_var1, '%Y-%m-%d %H:%M:%S')
            if (int(date_time_obj1.strftime('%Y%m%d')) == today_date) or (int(date_time_obj1.strftime('%Y%m%d')) >= today_date):
                forcast_data_list[today_date] = {}
                forcast_data_list[today_date]['day'] = str(date_time_obj1.strftime('%A'))[0:3]
                forcast_data_list[today_date]['temperature'] = city_weather['list'][c]['main']['temp']
                forcast_data_list[today_date]['temperature_max'] = city_weather['list'][c]['main']['temp_max']
                forcast_data_list[today_date]['temperature_min'] = city_weather['list'][c]['main']['temp_min']

                forcast_data_list[today_date]['description'] = city_weather['list'][c]['weather'][0]['description']
                forcast_data_list[today_date]['icon'] = city_weather['list'][c]['weather'][0]['icon']
                forcast_data_list[today_date]['city'] = city_weather['city']['name']
                # forcast_data_list[today_date]['country'] = city['city']['country']
                dt =dt+datetime.timedelta(days=1)

                today_date = int(dt.strftime('%Y%m%d'))
            else:
                pass
        city_list.append({'name':city.name,'country':city_weather['city']['country']})
        data_list.append(forcast_data_list)
    context = {'data_list':data_list,'form':form,'city_list':city_list}
    return render(request, 'weather.html',context) #returns the index.html template