from django.utils import translation


def kelvin_to_celsius(kelvin):
    return "{}".format(round(kelvin - 273.15))


def change_language(request, lang):
    user_language = lang
    translation.activate(user_language)
    request.session[translation.LANGUAGE_SESSION_KEY] = user_language


def process_weather(list_values):
    import datetime
    assert type(list_values) == list
    utc = str(datetime.datetime.utcnow().date())
    today = str(datetime.datetime.now().date())
    date = today
    max_temp = -1
    min_temp = 100000
    result = {}
    result['list'] = []
    list_data = {}
    result['today'] = []
    today_data = {}
    counter = 0

    for item in list_values:
        # item_date = item['dt_txt'].split(' ')[0]
        item_date = datetime.datetime.fromtimestamp(
                 int(item['dt'])
        ).strftime('%Y-%m-%d')

        if item_date == today:
            today_data['timestamp'] = int(item['dt']) - 21600
            today_data['exact_time'] = item['dt_txt'].split(' ')[1]
            today_data['temp'] = kelvin_to_celsius(item['main']['temp'])
            today_data['type'] = item['weather'][0]['main']
            today_data['icon'] = item['weather'][0]['icon']
            result['today'].append(today_data)
            today_data = {}
        if item_date == date:
            if item['main']['temp_max'] > max_temp:
                max_temp = item['main']['temp_max']
            if item['main']['temp_min'] < min_temp:
                min_temp = item['main']['temp_min']
        else:
            list_data['timestamp'] = int(item_date_timestamp) - 21600
            # datetime.datetime.fromtimestamp(
            #     int("1284101485")
            # ).strftime('%Y-%m-%d %H:%M:%S')
            list_data['date'] = date
            list_data['temp'] = {
                'max': kelvin_to_celsius(max_temp),
                'min': kelvin_to_celsius(min_temp)
            }
            max_temp = -1
            min_temp = 100000
            result['list'].append(list_data)
            list_data = {}
            # date = item['dt_txt'].split(' ')[0]
            date = datetime.datetime.fromtimestamp(
                 int(item['dt'])
            ).strftime('%Y-%m-%d')
            if item['main']['temp_max'] > max_temp:
                max_temp = item['main']['temp_max']
            if item['main']['temp_min'] < min_temp:
                min_temp = item['main']['temp_min']

        item_date_timestamp = item['dt']
        counter += 1
        if counter == len(list_values):
            list_data['timestamp'] = item_date_timestamp
            list_data['date'] = date
            list_data['temp'] = {
                'max': kelvin_to_celsius(max_temp),
                'min': kelvin_to_celsius(min_temp)
            }
            result['list'].append(list_data)
    return result


def language_activate(request, language='ru'):
    if language == 'ky':
        language = 'kg'
    translation.activate(language)
    request.session[translation.LANGUAGE_SESSION_KEY] = language


def new_weather_fetch_view(self, request, *args, **kwargs):
    pass


def fahrenheit_to_celsius(fahrenheit):
    return "{}".format(round((fahrenheit - 32) * .5556))


def accuweather_five_day_result_process(list_values):
    result_list = []
    item_data = {}
    temp = {}

    for item in list_values:
        item_data['date'] = item['Date'].split('T')[0]
        temp['max'] = fahrenheit_to_celsius(item['Temperature']['Maximum']['Value'])
        temp['min'] = fahrenheit_to_celsius(item['Temperature']['Minimum']['Value'])
        item_data['temp'] = temp
        item_data['timestamp'] = item['EpochDate']
        result_list.append(item_data)
        item_data = {}
        temp = {}

    return result_list


def accuweather_one_day_result_process(list_values):
    import datetime
    result_list = []
    item_data = {}
    today = str(datetime.datetime.now().date())

    for item in list_values:
        date = item['DateTime'].split('T')[0]
        if today == date:
            item_data['icon'] = item['WeatherIcon']
            item_data['temp'] = fahrenheit_to_celsius(item['Temperature']['Value'])
            item_data['type'] = item['IconPhrase']
            item_data['timestamp'] = item['EpochDateTime']
            item_data['exact_time'] = (item['DateTime'].split('T'))[1].split('+')[0]
            result_list.append(item_data)
            item_data = {}
    return result_list
