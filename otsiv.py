import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

URL = 'http://ucheba-otziv.ru/opinion/opinion_93.html'

page = requests.get(URL)

#print(page.text)

soup = BeautifulSoup(page.text, 'html.parser')

reviews = soup.find_all('td', class_ = 'short_descr')



pattern1 = r'\d{1,2}\s\w+\s\d{4}\s\w+'
pattern2 = r'\d{2}[:]\d{2}'
pattern3 = r'(\n)\w+(\n)'
pattern4len = r'\d{1,2}\s\w+\s\d{4}\s\w+\s[в]\s\d{2}[:]\d{2}'

date_review_list = [] # создаем список для дат
time_review_list = [] # создаем список для времени комментария
reviews_list = [] # список с текстами комментариев

dict_review = dict.fromkeys(['Дата', 'Время', 'Сайт', 'Отзыв'])


for rev in reviews:
    #print(rev.text)
    txt_str = str(rev.text) # преобразуем rev.text в строку
    #print(txt_str)

    date_review = re.findall(pattern1, txt_str) # ищем дату по шаблону
    time_review = re.findall(pattern2, txt_str) # ищем время по шаблону
    len_date_time = re.findall(pattern4len, txt_str) # использем шаблон дата-время(первая строка), чтобы посчитать длину строки и потом "удалить" ее
    len_date_time_str = str(len_date_time)
    #print(time_review)
    date_review_str = str(date_review)
    date_review_str = date_review_str[2:(len(date_review_str)-2)] # избавляемся от скобок и кавычек
    #print(date_review_str)
    time_review_str = str(time_review)
    time_review_str = time_review_str[2:len(time_review_str)-2] # избавляемся от скобок и кавычек


    #print(date_review_str)
    #print(type(date_review_str))
    midlen = len(len_date_time_str) # длина первой строки (дата-время), от которой необходимо "избавиться", чтобы получить комменатрий
    descr_review = txt_str[midlen:] # получаем комментарий
    descr_review = descr_review[1:len(descr_review)-2] # очищаем комменатрий от кавычек и скобок


    date_review_list.append(date_review_str) # заполняем датами список дат
    time_review_list.append(time_review_str) # заполняем временем список со временем
    reviews_list.append(descr_review) # заполняем комменатриями список комменатриев

# заполняем словарь
dict_review['Дата'] = date_review_list
dict_review['Время'] = time_review_list
dict_review['Отзыв'] = reviews_list
dict_review['Сайт'] = 'ucheba-otziv.ru'


#print(date_review_list)
#print(reviews_list)
#print(dict_review)

# используя pandas, формируем DataFrame
df = pd.DataFrame(dict_review)
#print(df)
#print(df['Время'])

df.to_csv('df.csv') # создаем csv


# читаем csv
#DataFrame_from_csv = pd.read_csv('df.csv')
#print(type(DataFrame_from_csv))
#print(DataFrame_from_csv)

