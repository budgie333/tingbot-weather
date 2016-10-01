import tingbot
from tingbot import *
import urllib2
import json
import time


temperature_str = "n/a"
description_str = ""
icon_str = "icons/na.png"
screen_index = 0
max_screens = 3
forecast_list = []

# list of location informaiton [0] = city, [1] = state, [2] = country
location = ["New York", "NY", "USA"]

# update screen primarily displaying time
def update_time_screen (current_time, current_date):
    
    global temperature_str
    global icon_str
    
    screen.fill (color='black')
    screen.text (temperature_str, align="topright", color="white", font_size=35)
    screen.text (current_time, align="center", color="white", font_size=65)
    screen.text (current_date, align="bottom", color="white", font_size=25)
    if len (icon_str) > 0:
        screen.image (icon_str, align='topleft', scale='fit', max_width=75, max_height=75)


# update screen primarily displaying current weather
def update_weather_screen (current_time):
    
    global temperature_str
    global icon_str
    global description_str
    
    screen.fill (color='black')
    screen.text (current_time, align="topright", color="white", font_size=35)
    screen.text (temperature_str, align="center", color="white", font_size=70)
    if len (forecast_list) > 0:
        hi_lo = forecast_list [0][1] + " / " + forecast_list [0][2]
        screen.text (hi_lo, align="center", color="white", xy=(160,180), font_size=25)
    screen.text (description_str, align="bottom", color="white", font_size=25)
    if len (icon_str) > 0:
        screen.image (icon_str, align="topleft", scale='fit', max_width=150, max_height=150)


# update screen displaying multi day forecast
def update_forecast_screen ():
    
    screen.fill (color='black')
    if len (forecast_list) == 0:
        screen.text ("forecast unavailable", align="top", color="white", font_size=30)
        return
    
    stop = min (len (forecast_list), 4)
    screen.text (str (stop) + " day forecast", align="top", color="white", font_size=30)
    for i in range (0, stop):
        forecast = forecast_list [i]
        # create string <day> <high> <low> <desc>
        line = forecast [0] + ":\t" + forecast [1] + "/" + forecast [2] + "\t" + forecast [3]
        screen.text (line, align="left", xy=(0, (i+1) * 55), color="white", font_size = 20)
        if code_to_icon_map.has_key (forecast [4]):
            icon_str = code_to_icon_map [forecast [4]]
        else:
            icon_str = "icons/na.png"
        # alignment is relative to xy, xy with topright alignment makes xy the topright point in the icon
        screen.image (icon_str, align="right", xy=(320, (i+1) * 55), scale='fit', max_width=75, max_height=75)


# move to next screen    
@right_button.press
def screen_right ():
    
    global screen_index
    
    screen_index += 1
    if screen_index >= max_screens:
        screen_index = 0


# decrease brightness by 5
@midleft_button.press
def screen_midleft ():
    
    brightness = screen.brightness

    brightness -= 5
    if brightness < 0:
        brightness = 0
        
    screen.brightness = brightness
    
    screen.rectangle (align='center', size=(280,40), color='black')
    screen.text ("Brightness " + str (brightness), align='center')


# increase brightness by 5
@midright_button.press
def screen_midright ():
    
    brightness = screen.brightness

    brightness += 5
    if brightness > 100:
        brightness = 100
        
    screen.brightness = brightness
    
    screen.rectangle (align='center', size=(280,40), color='black')
    screen.text ("Brightness " + str (brightness), align='center')


# move to previous screen
@left_button.press
def screen_left ():
    
    global screen_index
    
    if screen_index == 0:
        screen_index = max_screens - 1
    else:
        screen_index -= 1


# update temperature from yahoo
@every(minutes=15.0)
def update_temperature_data_yahoo ():

    city = location [0].replace (" ", "%20")
    state = location [1].replace (" ", "%20")
    country = location [2].replace (" ", "%20")
    url_string = "https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20weather.forecast%20where%20woeid%20in%20(select%20woeid%20from%20geo.places(1)%20where%20text%3D%22" + city + "%2C%20" + state + "%2C%20" + country + "%22)&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys"
    response = urllib2.urlopen (url_string).read ()

    response_dict = json.loads (response)
    
    global temperature_str
    global description_str
    global icon_str
    global forecast_list
    
    try:
        temperature_str = response_dict['query']['results']['channel']['item']['condition']['temp'] + " F"
        description_str = response_dict['query']['results']['channel']['item']['condition']['text']
        code = int (response_dict['query']['results']['channel']['item']['condition']['code'])
        #icon_str = "http://l.yimg.com/a/i/us/we/52/" + str (code) + ".gif"
        if code_to_icon_map.has_key (code):
            icon_str = code_to_icon_map [code]
        else:
            icon_str = "icons/na.png"
        forecast = response_dict['query']['results']['channel']['item']['forecast']
        forecast_list = [] # clear current forecast_list
        for element in forecast:
            #tup = (day, high, low, text, code)
            tup = (element ["day"], element["high"], element["low"], element["text"], int (element["code"]))
            forecast_list.append (tup)
    except:
        temperature_str = ""
        description_str = "error"
        icon_str = "icons/na.png"


# primary update function, calls screen specific update
@every(seconds=1.0)
def update_screen():
    current_time = time.strftime ("%I:%M %p")
    current_time = current_time.strip ('0') # remove leading 0 from 12 hour format
    current_date = time.strftime ("%b %d, %Y")
    
    if screen_index == 0: # time screen
        update_time_screen (current_time, current_date)
    elif screen_index == 1: # current weather
        update_weather_screen (current_time)
    else: # forecast
        update_forecast_screen ()

    
# called once to initialize brightness
@once (seconds=0.25)
def on_startup ():
    screen.brightness = 75


# map of weather code to icon png
code_to_icon_map = {
    0: 'icons/0.png', #  tornado
    1: 'icons/1.png', #  tropical storm
    2: 'icons/2.png', #  hurricane
    3: 'icons/3.png', #  severe thunderstorms
    4: 'icons/4.png', #  thunderstorms
    5: 'icons/5.png', #  mixed rain and snow
    6: 'icons/6.png', #  mixed rain and sleet
    7: 'icons/7.png', #  mixed snow and sleet
    8: 'icons/8.png', #  freezing drizzle
    9: 'icons/9.png', #  drizzle
    10: 'icons/10.png', #  freezing rain
    11: 'icons/11.png', #  showers
    12: 'icons/12.png', #  showers
    13: 'icons/13.png', #  snow flurries
    14: 'icons/14.png', #  light snow showers
    15: 'icons/15.png', #  blowing snow
    16: 'icons/16.png', #  snow
    17: 'icons/17.png', #  hail
    18: 'icons/18.png', #  sleet
    19: 'icons/19.png', #  dust
    20: 'icons/20.png', #  foggy
    21: 'icons/21.png', #  haze
    22: 'icons/22.png', #  smoky
    23: 'icons/23.png', #  blustery
    24: 'icons/24.png', #  windy
    25: 'icons/25.png', #  cold
    26: 'icons/26.png', #  cloudy
    27: 'icons/27.png', #  mostly cloudy (night)
    28: 'icons/28.png', #  mostly cloudy (day)
    29: 'icons/29.png', #  partly cloudy (night)
    30: 'icons/30.png', #  partly cloudy (day)
    31: 'icons/31.png', #  clear (night)
    32: 'icons/32.png', #  sunny
    33: 'icons/33.png', #  fair (night)
    34: 'icons/34.png', #  fair (day)
    35: 'icons/35.png', #  mixed rain and hail
    36: 'icons/36.png', #  hot
    37: 'icons/37.png', #  isolated thunderstorms
    38: 'icons/38.png', #  scattered thunderstorms
    39: 'icons/39.png', #  scattered thunderstorms
    40: 'icons/40.png', #  scattered showers
    41: 'icons/41.png', #  heavy snow
    42: 'icons/42.png', #  scattered snow showers
    43: 'icons/43.png', #  heavy snow
    44: 'icons/44.png', #  partly cloudy
    45: 'icons/45.png', #  thundershowers
    46: 'icons/46.png', #  snow showers
    47: 'icons/47.png', #  isolated thundershowers
}

tingbot.run()
