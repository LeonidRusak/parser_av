import requests
from bs4 import BeautifulSoup
from datetime import datetime

url = 'https://cars.av.by/filter?brands[0][brand]=989&brands[0][model]=996&brands[0][generation]=1997&' \
      'transmission_type=2&body_type[0]=3&engine_type[0]=5'

response = requests.get(url)
bs = BeautifulSoup(response.text, 'html.parser')

temp_car = bs.findAll('h3', class_='listing-item__title')  # Нахождение всех объявлений, удовлетворяющих запросу
data = list(temp_car)

list_id = []  # Список id найденных авто по фильтру на сайте

for i in data:  # Выделение id объявления на сайте и добавление его в список
    a = str(i)
    a = a[69:90]
    list_id.append(a)

temp_price = bs.findAll('div', class_='listing-item__priceusd')  # Цена авто
data = list(temp_price)

list_price = []

for i in data:
    a = str(i)
    a = a[38] + a[40:43]
    list_price.append(a)

temp_year = bs.findAll('div', class_='listing-item__params')  # Год выпуска авто
data = list(temp_year)

list_year = []

for i in data:
    a = str(i)
    a = a[39:43]
    list_year.append(a)

temp_mileage = bs.findAll('div', class_='listing-item__params')  # Пробег авто
data = list(temp_mileage)

list_mileage = []

for i in data:
    a = str(i)
    a = a[160:163] + a[164:167]
    list_mileage.append(a)

list_final = []  # Итоговый список с найденными объявлениями
num_ad = 1  # Номер объявления в полученном списке

for i in list_id:  # Добавление ссылки на авто
    list_final.append(f'{num_ad}. ' + 'https://cars.av.by/' + i)
    num_ad += 1

count = 0
for i in list_price:  # Добавление цены авто
    list_final[count] = list_final[count] + ' цена: ' + i + '$'
    count += 1

count = 0
for i in list_year:  # Добавление года выпуска авто
    list_final[count] = list_final[count] + ' год выпуска: ' + i
    count += 1

count = 0
for i in list_mileage:  # Добавление пробега авто
    list_final[count] = list_final[count] + ' пробег: ' + i + 'км'
    count += 1

"""
Для удобного понимания информации в генерируемом текстовом файле, в шапку добавим описание.
Полученный список запишется в файл построчно для удобства чтения 
"""
list_final.insert(0, f'Список актуальных объявлений на {datetime.now()}')
list_final.insert(1, 'Марка: Peugeot Модель: 307 I Двигатель: Дизель 2.0 КПП: механика Кузов: Хэтчбек 5дв.')

file_text = open('parser.txt', 'w', encoding='utf-8')
for i in list_final:
    file_text.write(i)
    file_text.write('\n')
file_text.close()
