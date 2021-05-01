import urllib.request
import json
from django.shortcuts import render

# Create your views here.


def home(request):
    #If we have post data get the city name the user inputed
    if request.method == 'POST':
        c = request.POST['city']
        # declare variable city and replace the space in between city name with a '+'
        city = c.replace(" ", "+")

        #Declare variable source that contains all jason data from the api
        source = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?q='+city+'&units=metric&appid=0a9ad62456c4ac76f7aeb14331d20255').read()
        list_of_data = json.loads(source)

        #Longitude and Latitude possition of the city
        lon = str(list_of_data['coord']['lon'])
        lat = str(list_of_data['coord']['lat'])

        #Our Air quality api source
        air_source = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/air_pollution?lat='+lat+'&lon='+lon+'&appid=0a9ad62456c4ac76f7aeb14331d20255').read()
        list_of_air = json.loads(air_source)

        #air quality variable
        quality = str(list_of_air['list'][0]['main']['aqi'])

        pollution = ''
        #Air quality is represented by numbers from 1 - 4
        #I represented the numbers with words to be more clear
        if quality == '1':
            pollution = 'Good'
        elif quality == '2':
            pollution = 'Fair'
        elif quality == '3':
            pollution = 'Moderate'
        elif quality == '4':
            pollution = 'Poor'
        else:
            pollution = 'Very Poor'

        #Data dictionary that contains everything to be rendered on the html page
        data = {
            'city': city,
            "country_code": str(list_of_data['sys']['country']),
            'long': lon,
            'lat': lat, 
            'temperature':str(list_of_data['main']['temp']) + '°C',
            'pressure':str(list_of_data['main']['pressure']),
            'humidity':str(list_of_data['main']['humidity']),
            'air':pollution
        }
        
        print(data)
    else:
        data = {}
    
    return render(request, 'weatherApp/home.html', data)
