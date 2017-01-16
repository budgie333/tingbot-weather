# weather_clock

Create a **settings.json** with the following settings:
```
{
    "city":"",
    "state":"",
    "country":"",
    "source":"",
    "appid":"",
    "brightness":
        {
            "11:00 PM":15,
            "08:00 AM":75,
            "startup":75
        }
}
```
weather app with multiple screens; clock, current temp and mutli day forecast

navigate screens via left and right buttons

increase and decrease screen brightness via midleft and midright buttons

'city', 'state and 'country' settings are required.

'source' is either 'yahoo' or 'openweather', defaults to 'yahoo'.  This determines the source of the weather information

'appid' is required if using 'openweather' as source.  This ID is obtained from the openweathermap website for individual users.

'brightness' is an optional setting that allows the app to auto adjust the brightness based on time.  Setting 'startup' will set the brightness to that level when the app is started.

icons used from http://vclouds.deviantart.com/gallery/#/d2ynulp
