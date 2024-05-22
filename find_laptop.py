import pandas as pd
import telebot
import spacy
import clearml
from clearml import Task

# Установить ключ API вашего проекта
task1 = Task.init(project_name='Подбор ноутбука', task_name='Laptops')

nlp = spacy.load("ru_core_news_md")
# nlp = spacy.load("en_core_web_md")

bot = telebot.TeleBot('7010978135:AAEh_urIyQSOPnbN2E3Rizqx5v8Nzp8KqTE')


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if (message.text == '/start') | (message.text == '/help'):
        bot.send_message(message.from_user.id, "Введите запрос")
    else:
        user_query = message.text
        recommended_notebooks = find_matching_notebooks1(user_query, data)
        if recommended_notebooks:
            bot.send_message(message.from_user.id, "Рекомендуемые ноутбуки:")
            i = 1
            for notebook in recommended_notebooks:
                bot.send_message(message.from_user.id,
                                 notebook['Manufacturer'] + ' ' + notebook['Model Name'] + ' ' + notebook[
                                     'Category'] + ' #Screen Size= ' + str(
                                     notebook['Screen Size']) + ' #Weight= ' + str(notebook['Weight']))
                i += 1
                if (i > 10):
                    break
        else:
            bot.send_message(message.from_user.id, "Извините, не удалось найти подходящие ноутбуки.")


# Загрузить данные из базы данных
data = pd.read_excel("C:/Users/Ильшат/Downloads/обновленный_файл.xlsx")

# Convert 'Weight' column to numeric
data['Weight'] = pd.to_numeric(data['Weight'], errors='coerce')


# Функция для поиска ноутбуков по признакам ru
def find_matching_notebooks1(user_query, data):
    matching_notebooks = []
    ctg = ('легкий небольшой дешевый классический ультрабук игровой')
    lst_ctg = ctg.split()
    user_query = user_query.lower()
    lst = user_query.split()
    query = ''
    for word in lst:
        if word != 'ноутбук':
            doc1 = nlp(word)
            ctg_elem = ''
            max = 0
            for c in lst_ctg:
                doc2 = nlp(c)
                # print(doc1.similarity(doc2))
                if doc1.similarity(doc2) > max:
                    max = doc1.similarity(doc2)
                    ctg_elem = c
            if max > 0.2:
                query += ctg_elem
                query += ' '
    print(query)
    user_query = query

    if user_query == '':
        return matching_notebooks

    for index, notebook in data.iterrows():
        try:
            conditions = []
            if 'легкий' in user_query:
                conditions.append(1 <= notebook['Weight'] <= 2)
            if 'небольшой' in user_query:
                conditions.append(notebook['Screen Size'] <= 15.4 and notebook['Weight'] <= 3)
            if 'дешевый' in user_query:
                conditions.append(float(notebook['Price (Euros)'].replace(',', '.')) <= 1000)
            if 'классический' in user_query:
                conditions.append(notebook['Category'] == 'notebook')
            if 'ультрабук' in user_query:
                conditions.append(notebook['Category'] == 'ultrabook')
            if 'игровой' in user_query:
                conditions.append(notebook['Category'] == 'gaming')

            if all(conditions):
                matching_notebooks.append(notebook)
        except ValueError:
            print(f"Не удалось преобразовать вес в числовой формат: {notebook['Weight']}")

    return matching_notebooks


# Функция для поиска ноутбуков по признакам eng
def find_matching_notebooks2(user_query, data):
    matching_notebooks = []
    ctg = ('lightweight small cheap ultrabook classic gaming')
    lst_ctg = ctg.split()
    user_query = user_query.lower()
    lst = user_query.split()
    query = ''
    for word in lst:
        if word != 'notebook':
            doc1 = nlp(word)
            ctg_elem = ''
            max = 0
            for c in lst_ctg:
                doc2 = nlp(c)
                # print(doc1.similarity(doc2))
                if doc1.similarity(doc2) > max:
                    max = doc1.similarity(doc2)
                    ctg_elem = c
            if max > 0.2:
                query += ctg_elem
                query += ' '
    print(query)
    user_query = query

    for index, notebook in data.iterrows():
        try:
            conditions = []
            if 'lightweight' in user_query:
                conditions.append(1 <= notebook['Weight'] <= 2)
            if 'small' in user_query:
                conditions.append(notebook['Screen Size'] <= 15.4 and notebook['Weight'] <= 3)
            if 'cheap' in user_query:
                conditions.append(float(notebook['Price (Euros)'].replace(',', '.')) <= 1000)
            if 'classic' in user_query:
                conditions.append(notebook['Category'] == 'notebook')
            if 'ultrabook' in user_query:
                conditions.append(notebook['Category'] == 'ultrabook')
            if 'gaming' in user_query:
                conditions.append(notebook['Category'] == 'gaming')

            if all(conditions):
                matching_notebooks.append(notebook)
        except ValueError:
            print(f"Не удалось преобразовать вес в числовой формат: {notebook['Weight']}")

    return matching_notebooks


# Рекомендация ноутбуков для пользователя
bot.polling(none_stop=True, interval=0)
