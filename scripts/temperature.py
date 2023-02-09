import requests
from bs4 import BeautifulSoup
# import bot
import telebot

bot = telebot.TeleBot('5761545857:AAFqY-qTVm9b4QjOyq8HWYIv5wBWvZfJG20')

# city -> temperature
def main (city):
    
    bot.send_message(364623079, city)
    return city

    lan_lon = coordsRU(city)
    if lan_lon == 404:
        return 404

    temperature = temp(lan_lon[0],lan_lon[1])
        
    # print('def t output: '+str(temperature))
    return temperature
    

# city -> coords
def coordsRU(city):

    # city -> url -> xml
    global API
    url = 'https://geocode-maps.yandex.ru/1.x/?apikey={}&geocode={}'.format(API[0], city)
    print(url)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, features='xml')

    # real city name log in console
    if soup.find('LocalityName') != None:
        print('city name: '+soup.find('LocalityName').text)
    elif soup.find('AdministrativeAreaName') != None:
        print('city name: '+soup.find('AdministrativeAreaName').text)

    # xml -> <pos> tags
    coords_raw = soup.find_all('pos')
    if coords_raw == None:
        return 404
    
    # <pos> tags -> [[<pos> tag1], [<pos> tag2],..] -> [[lat1],[long1], [lat2],[long2],..]
    coords = []
    i = 0
    for c in coords_raw:
        coords.append(i)
        coords[i] = c.text.split()
        i += 1
        print('c'+str(i)+': '+str(c))

    print('\n'+str(coords))
    # return latitude, longitude

    # для работы нужно сделать сортировку листов в листах и устранить погрешности в +-2
    #                  выводить в бота запрос о том, какой именно город нужен юзеру
    #                  сделать на каждый город по кнопке
    #                  и уже выбранный юзером город отправлять в def temp ниже


# coords -> temperature
def temp(latitude, longitude):    
    bot = telebot.TeleBot(API[1])

    # getting access to url
    url = 'https://yandex.ru/pogoda/?lat={}&lon={}'.format(latitude, longitude)
    print(url)
    page = requests.get(url)
    print('url access: '+str(page.status_code))

    # xml -> bs4
    soup = BeautifulSoup(page.text, features='lxml')

    # parsing 
    t_raw = soup.find('span', class_='temp__value temp__value_with-unit')

    # антикраш при ненаходе
    if t_raw == None:
        return 404
    
    # конвертация str -> float
    temperature = t_raw.text
    print('def temp output: '+str(t_raw))

    return temperature


# city -> coords
# OUTDATED (used en.wiki.org)

# def coordsEN(city):

    url = 'https://en.wikipedia.org/wiki/' + city
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    coords_raw = soup.find('span', class_='latitude')     # поиск широты на странице википедии с помощью bs4
    longitude_raw = soup.find('span', class_='longitude')   # поиск долготы на странице википедии с помощью bs4

    if coords_raw == None:
        return 404

    latitude_str = coords_raw.text.replace('°', '.')      # float'ование string'а
    latitude_str = latitude_str[:latitude_str.index('.')+2]
    longitude_str = longitude_raw.text.replace('°', '.')    # float'ование string'а
    longitude_str = longitude_str[:longitude_str.index('.')+2]

    latitude = float(latitude_str)                          # конвертация str -> float
    longitude = float(longitude_str)                        # конвертация str -> float

    return latitude, longitude


#     [yandexGEO, tgBOT]
API = ['9561ddad-b4b1-4260-b2a4-2c1f70d44e60', '5761545857:AAFqY-qTVm9b4QjOyq8HWYIv5wBWvZfJG20']
# Надо бы в отдельное место сунуть какое-нибудь, да каждую апишку нормально обозвать

# for script testing
# print('\nOutput: '+str(coordsRU('лондон')))