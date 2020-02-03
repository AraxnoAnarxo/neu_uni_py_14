import requests
from bs4 import BeautifulSoup
import re
import pandas as pd


URL = 'https://professorrating.org/university.php?id=168'

page = requests.get(URL)

#print(page.text)

soup = BeautifulSoup(page.text, 'html.parser')

reviews = soup.find_all('div', class_ = 'text-comment')

pattern_date = r'\d{2}\s\w+\s\d{4}'
pattern_time = r'\d{2}[:]\d{2}'

date_list = [] # список с датами
time_list = [] # список со временм комменатрия
reviews_list = [] # список с комменатриями
dict_review = dict.fromkeys(['Дата', 'Время', 'Отзыв']) # создаем словарь



for rev in reviews:
    #print(rev.text)
    text_str = str(rev.text)
    #print(text_str)
    date_review = re.findall(pattern_date, text_str) # ищем дату по шаблону
    date_review_str = str(date_review)

    time_review = re.findall(pattern_time, text_str) # ищем время по шаблону
    #print(type(time_review))
    time_review_str = str(time_review)
    #time_rev = re.sub(r'[[\']',"", time_review_str)

    time_review_str = time_review_str[2:(len(time_review_str)-2)] # избавляемся от скобок и кавычек
    #print(time_review_str)


    date_review_new_01 = date_review_str[2:len(date_review_str)-2] # избавляемся от скобок и кавычек
    date_review_02 = date_review_new_01.replace('\\xa0', ' ') # избавляемся от знаков \xa0
    date_list.append(date_review_02) # формируем список с датами
    time_list.append(time_review_str) # формируем список со временем

    # Текст комменатрия

    text_str_re = re.split(r'Пожаловаться', text_str) # используем re.split, чтобы разделить строку по слову, после которого начинается комментарий
    text_str_comment = str(text_str_re[1]) # выбираем часть из списка, в которой хранится комменарий
    text_review = re.sub(r'[+]\d{1,5}', "", text_str_comment) # избавляемся от лишних симоволов (типа +150)
    # print(text_review)
    reviews_list.append(text_review) # формируем список с комментариями

# заполняем словарь
dict_review['Дата'] = date_list
dict_review['Время'] = time_list
dict_review['Отзыв'] = reviews_list

#print(dict_review)
# print(len(date_list))
# print(len(time_list))
# print(len(reviews_list))


# используя pandas, создаем DataFrame
df = pd.DataFrame(dict_review)
print(df)

# формируем файл csv
df.to_csv('df_02.csv')

# читаем csv

# читаем csv
DataFrame_from_csv = pd.read_csv('df_02.csv')
print(DataFrame_from_csv)



