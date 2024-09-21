import urequests
import ujson as json
import gc


class open_weather_map():
    def __init__(self, country, city, key):
        self.country_code = country
        self.city_code = city
        self.api_key = key
        gc.enable()
        gc.collect()

        
    def connect_url(self):
        gc.collect()
        url = 'https://api.openweathermap.org/data/2.5/weather?q=' + self.city_code + ',' + self.country_code + '&APPID=' + self.api_key + '&units=metric'
        return url
    
    
    def fetch_data(self):
        return_data = []
        
        fetched_data = urequests.post(self.connect_url())
        
        gc.collect()
        return_data.append(fetched_data.json().get('name'))                                # 0
        return_data.append(fetched_data.json().get('sys').get('country'))                  # 1
        return_data.append(fetched_data.json().get('coord').get('lat'))                    # 2
        return_data.append(fetched_data.json().get('coord').get('lon'))                    # 3
        
        return_data.append(fetched_data.json().get('dt'))                                  # 4
        return_data.append(fetched_data.json().get('sys').get('sunrise'))                  # 5
        return_data.append(fetched_data.json().get('sys').get('sunset'))                   # 6
        
        return_data.append(fetched_data.json().get('weather')[0].get('main'))              # 7
        return_data.append(fetched_data.json().get('weather')[0].get('description'))       # 8
        
        return_data.append(fetched_data.json().get('main').get('temp'))                    # 9
        return_data.append(fetched_data.json().get('main').get('feels_like'))              # 10
        return_data.append(fetched_data.json().get('main').get('temp_min'))                # 11
        return_data.append(fetched_data.json().get('main').get('temp_max'))                # 12
        
        return_data.append(fetched_data.json().get('main').get('humidity'))                # 13
        
        return_data.append(fetched_data.json().get('main').get('pressure'))                # 14
        
        return_data.append(fetched_data.json().get('wind').get('speed'))                   # 15
        return_data.append(fetched_data.json().get('wind').get('deg'))                     # 16
        return_data.append(fetched_data.json().get('wind').get('gust'))                    # 17
        
        return_data.append(fetched_data.json().get('visibility'))                          # 18
        
        return_data.append(fetched_data.json().get('clouds').get('all'))                   # 19
        
        return_data.append(fetched_data.json().get('main').get('sea_level'))               # 20
        return_data.append(fetched_data.json().get('main').get('grnd_level'))              # 21
        
        return_data.append(fetched_data.json().get('weather')[0].get('icon'))              # 22

        return return_data
