import math
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Определение количество страниц пагинации в запросе по определенной модели автомобиля
# В случае получения ошибки при запросе, повторяем сам запрос пока не получим нужный результат

while True:
    try:
        url = 'https://cars.av.by/peugeot/307'
        response = requests.get(url)
        bs = BeautifulSoup(response.text, 'html.parser')

        car = bs.findAll('h3', class_='listing__title')  # Нахождение количества объявлений, удовлетворяющих запросу
        count = math.ceil(int(str(car)[52:55]) / 25)  # Количество страниц пагинации по нашему запросу
        break
    except Exception:
        continue


data_id = []  # Список с id найденных объявлений
data_price = []  # Список с ценами автомобилей в найденных объявлениях
data_year = []  # Список с годами выпуска автомобилей
data_mileage = []  # Список с пробегами автомобилей, указанных в объявлении

for i in range(1, count+1):
    url = f'https://cars.av.by/filter?brands[0][brand]=989&brands[0][model]=996&page={i}&sort=4'
    response = requests.get(url)
    bs = BeautifulSoup(response.text, 'html.parser')
    # Нахождение всех id объявлений, удовлетворяющих запросу
    car_id = bs.findAll('a', class_='listing-item__link')
    data_id += list(car_id)
    car_price = bs.findAll('div', class_='listing-item__priceusd')
    data_price += list(car_price)
    car_year = bs.findAll('div', class_='listing-item__params')
    data_year += list(car_year)
    data_mileage += list(car_year)


list_final = []  # Итоговый список с найденными объявлениями
num_ad = 1  # Номер объявления в полученном списке

for i in range(len(data_id)):
    list_final.append(f'{num_ad}.' + ' ' + 'https://cars.av.by/' + str(data_id[i])[37:58] + ' цена: ' +
                      ''.join([i for i in str(data_price[i])[37:45] if i.isdigit()]) + '$, год выпуска: ' +
                      str(data_year[i])[39:43] + ', пробег: ' +
                      ''.join([i for i in str(data_mileage[i])[-29:-19] if i.isdigit()]) + 'км')
    num_ad += 1


"""
Для удобного понимания информации в генерируемом текстовом файле, в шапку добавлено описание.
Полученный список запишется в файл построчно для удобства чтения
"""
list_final.insert(0, f'Список актуальных объявлений на {datetime.now().strftime("%d-%m-%Y %H:%M:%S")}')
list_final.insert(1, 'Марка: Peugeot Модель: 307')

file_text = open('parser.txt', 'w', encoding='utf-8')
for i in list_final:
    file_text.write(i)
    file_text.write('\n')
file_text.close()
