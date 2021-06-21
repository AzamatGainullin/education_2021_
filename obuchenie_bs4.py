from bs4 import BeautifulSoup
import requests
import re

### ПОЛУЧЕНИЕ ИЗ ФАЙЛА ###
html_doc = """<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""
### ПОЛУЧЕНИЕ ИЗ ИНТЕРНЕТА ###
def get_html(url):
    r = requests.get(url)
    return r.text
html_doc = get_html('https://wordpress.org/')



soup = BeautifulSoup (html_doc, 'html.parser')

print(soup.prettify())


soup.title.text


soup.find_all('a')

for link in soup.find_all('a'):
    print(link.get('href'))


soup.get_text()

soup.section #извлекается первое вхождение тега
soup.section['class']

soup.find_all('section')[2]['class']

soup.find_all('section')[2].find('h2').text

Универсальный способ поиска по тегам любой вложенности,
любого повторяющегося числа тегов:
Ищем внутри любых тегов н-р <section>, если известно отличительное class == 'features':

for i in soup.find_all('section'):
    if i['class']==['features']:
        print(i.find('h2').text)

soup.find_all('section')[2].p.string


soup.section


stripped_strings достает любые тексты внути объекта супа, удаляя пробелы:

for string in soup.stripped_strings:
    print(repr(string))



метод next_siblings, применяемый к первому элементу уровня section,
позволяет перебрать все элементы данного уровня:

for sibling in soup.section.next_siblings:
    print(repr(sibling))


.find_all - работает только с тегами. Следующий код находит все теги в документе
(то есть исключает текст и т.п.):

for tag in soup.find_all(True):
    print(tag.name)


Использование своих функций для отбора тегов:
def has_href_and_data_title(tag):
    return tag.has_attr('href') and tag.has_attr('data-title')

soup.find_all(has_href_and_data_title)



Обновление универсального способа поиска по тегам любой вложенности,
любого повторяющегося числа тегов:
Ищем внутри любых тегов н-р <section>, если известно отличительное class == 'features':
))))). Но пока что находим только всю секцию:
soup.find_all("section", "features")

Любой нераспознанный аргумент будет превращен в фильтр по атрибуту тега.
Если вы передаете значение для аргумента с именем id,
Beautiful Soup будет фильтровать по атрибуту «id» каждого тега:
(кстати круто. по любому атрибуту найдет все что угодно)

soup.find_all(id="download")


Находит все, где есть href:
soup.find_all(href=True)


Если вы передадите значение для href, Beautiful Soup отфильтрует по атрибуту «href»
каждого тега:
soup.find_all(href=re.compile("face"))

И третий способ - используем нижнее подчеркивание class_:
soup.find_all("section", class_="features")


Помните, что один тег может иметь несколько значений для атрибута «class».


С помощью string вы можете искать строки вместо тегов.
soup.find_all(string=re.compile("Beautiful"))


Если относиться к объекту BeautifulSoup или объекту Tag так, будто это функция,
то это похоже на вызов find_all() ﻿с этим объектом.
soup(string=re.compile("Beautiful"))


first_link.find_next_siblings("a") - список все одноуровневых эелементов для "а".

Поддержка селекторов CSS.
soup.select("title")

soup.select('a[href]') - поиск по селектору для href работает лучше чем
просто find_all.
