import requests # для запроса кода страницы
from bs4 import BeautifulSoup # для парсинга нужной инфы
from scripts import api

# ???
import unicodedata

def u2a(text):
    return text.replace('\u2212', '-')

# city -> temperature
def main (city):

    # получаем все варианты координат
    lan_lon = coords(city)
    if lan_lon == 404:
        return 404

    # создаём словарь для вывода в бота
    coordsDict = {}

    # заполняем словарь по типу {coord:temp}
    i=0
    for l in lan_lon:
        print ('\nl', l)
        coordsDict[str(lan_lon[i])] = temp(lan_lon[i])
        i = i+1

    # наслаждаемся проделанной работой в консоли
    print ('\ncoordsDict = ', coordsDict)
    
    # тут будет как-то сделан вывод через кнопки
    # markup = types.InlineKeyboardMarkup()

    # for key, value in lan_lon.items():
    #     markup.add(types.InlineKeyboardButton(text=value,
    #                                         callback_data="['value', '" + value + "', '" + key + "']"),
    #             types.InlineKeyboardButton(text=crossIcon,
    #                                         callback_data="['key', '" + key + "']"))

    return(coordsDict)

    temperature = temp(lan_lon[0],lan_lon[1])
        
    return temperature
    

# city -> coords
def coords(city):

    # city -> url -> xml
    global API
    url = 'https://geocode-maps.yandex.ru/1.x/?apikey={}&geocode={}'.format(api.yaG(), city)
    print(url)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, features='xml')

    # real city name log in console
    if soup.find('LocalityName') != None:
        print('(LN) city name: '+soup.find('LocalityName').text+'\n')
    elif soup.find('AdministrativeAreaName') != None:
        print('(AAN) city name: '+soup.find('AdministrativeAreaName').text+'\n')
    # Возможно, где-то тут код может наебнуться, если не будет ни LocalityName, ни AdministrativeAreaName

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

    # float-ирование каждой координаты
    i = 0
    while i < len(coords):
        coords[i][0] = float(coords[i][0])
        coords[i][1] = float(coords[i][1])
        i += 1

    # Сортировка по возрастанию сначала первого числа, затем второго (если первое равно)
    print('\nПопытка сортировки')
    coords = sorted(coords)
    print(coords)

    # Удаление координат-дубликатов с погрешностью в 3
    print('\nУдаление лишних координат')
    i = 1
    while i < len(coords):
        if abs(coords[i][0] - coords[i-1][0]) < 3 or \
           abs(coords[i][1] - coords[i-1][1]) < 3:
            del coords[i]
        else: 
            i += 1 

    print("Output: ", coords)
    return coords


# coords -> temperature
def temp(latitude_and_longitude):    

    i = 1
    for l in latitude_and_longitude:

        # проверяем только нечётные позиции, т.к. если известна поз. 1, 
        # сразу можно узнать и поз. 2, не прогоняя цикл вновь лишний раз
        # делаем из ['lan','lon'] 'lan', 'lon'
        latitude = latitude_and_longitude[0]
        longitude = latitude_and_longitude[1]

        print('lat = ', latitude)
        print('lon = ', longitude)

        # getting access to url
        url = 'https://yandex.ru/pogoda/?lat={}&lon={}'.format(latitude, longitude)
        # url = 'https://api.weather.yandex.ru/v2/informers?apikey={}&lat={}&lon={}'.format(api.yaP(), latitude, longitude)
        print(url)
        page = requests.get(url)
        print('url access: '+str(page.status_code))

        # xml -> bs4
        soup = BeautifulSoup(page.text, features='lxml')

        # parsing 
        t_raw = soup.find('span', class_='temp__value temp__value_with-unit')
        t_captcha = soup.find('div', class_='CheckboxCaptcha-Status visuallyhidden')

        # антикраш при ненаходе
        if t_raw == None or t_captcha != None:
            if t_captcha == None:
                print(soup)
                return 404
            else: return '...' 
        
        # конвертация str -> float
        temperature = t_raw.text
        temperature = u2a(temperature)
        i += 2  

    print("Output: ", temperature)
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


# for script testing
# print('\nOutput: '+str(coordsRU('лондон')))