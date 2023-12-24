import telebot
import sqlite3
from telebot import types

TOKEN = "6694896807:AAEEZrKr5TIAITMOwHCoQA-RXNK2whBiVxw"
bot = telebot.TeleBot(TOKEN)

keyboard = types.InlineKeyboardMarkup(row_width=2)
BPMN_button = types.InlineKeyboardButton('Диаграмма BPMN', callback_data='bpmn')
dashboard_button = types.InlineKeyboardButton('Дашборд', callback_data='dashboard')
help_button = types.InlineKeyboardButton('Помощь', callback_data='help')
entry_button = types.InlineKeyboardButton('Записаться на мойку', callback_data='entry')
keyboard.add(BPMN_button, help_button, dashboard_button, entry_button)

@bot.message_handler(commands=['creator'])
def creator(message):
    bot.reply_to(message, 'Алексей 2ИБ-1')

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, 'Привет! Этот бот пощволяет записаться на мойку авто. '
                         'Отправьте /help, чтобы узнать доступные команды. Автор /creator')
@bot.message_handler(commands=['help'])

def help(message):
    bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=keyboard)

# Обработка кнопки 'Диаграмма BPMN'
def BPMN_but(message):
    bpmn_markup = types.InlineKeyboardMarkup(row_width=1)
    button9 = types.InlineKeyboardButton('Описание BPMN', callback_data='bpmn_function1')
    button10 = types.InlineKeyboardButton('Ссылка на диаграмму', callback_data='bpmn_function2')
    bpmn_markup.add(button9, button10)
    bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=bpmn_markup)

# кнопки для действий с Дашбордом
def Dashboard_but(message):
    dashboard_markup = types.InlineKeyboardMarkup(row_width=1)
    button1 = types.InlineKeyboardButton('Описание дашборда', callback_data='dashboard_function1')
    button2 = types.InlineKeyboardButton('Ссылка на GitHub', callback_data='dashboard_function2')
    dashboard_markup.add(button1, button2)
    bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=dashboard_markup)

# кнопки для действий с помощью
def Help_but(message):
    help_markup = types.InlineKeyboardMarkup(row_width=1)
    button15 = types.InlineKeyboardButton('Как пользоваться ботом', callback_data='help_function1')
    button16 = types.InlineKeyboardButton('Контакты поддержки', callback_data='help_function2')
    help_markup.add(button15, button16)
    bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=help_markup)

# кнопки для действий с оформлением заказа
def entry_but(message):
    entry_handler(message)

CALLBACK_D = {
    "Диаграмма BPMN": BPMN_but,
    "Дашборд": Dashboard_but,
    "Помощь": Help_but,
    "Оформить заказ": entry_but
     }

CALLBACK_D_BUTTON = {
    "bpmn": BPMN_but,
    "dashboard": Dashboard_but,
    "help": Help_but,
    "entry": entry_but,
     }

@bot.message_handler(func=lambda message: True)
def home_screen(message):
    if message.text in CALLBACK_D:
        CALLBACK_D[message.text](message)
    else:
        # Обработка иных сообщений
        bot.reply_to(message, 'Не понимаю /help', reply_markup=keyboard)

def entry_handler(message):
    bot.send_message(message.chat.id, 'Форма записи на мойку. Введите ваше имя:')
    bot.register_next_step_handler(message, enter_sender_name)

def enter_sender_name(message):
    entry = {}
    entry['sender_name'] = message.text
    bot.send_message(message.chat.id, f'Отлично, {message.text}! Теперь укажите жедаемую дату:')
    bot.register_next_step_handler(message, enter_data_entry, entry)

#Обработчик для ввода места подачи груза
def enter_data_entry(message, entry):
    entry['data_entry'] = message.text
    bot.send_message(message.chat.id, f'Дата записи: {message.text}. Теперь введите желаемое время:')
    bot.register_next_step_handler(message, enter_time_entry, entry)

#Обработчик для ввода пункта назначения
def enter_time_entry(message, entry):
    entry['time_entry'] = message.text
    # отчет
    report = f'Отчет по записи:\n' \
             f'Имя клиента: {entry["sender_name"]}\n' \
             f'Дата записи: {entry["data_entry"]}\n' \
             f'Время записи: {entry["time_entry"]}\n'

    # Отправка отчета пользователю
    bot.send_message(message.chat.id, report)
    # Создание подключения к базе данных SQLite
    conn = sqlite3.connect('entrys.db')
    cursor = conn.cursor()

    # Создание таблицы для заказов, если ее еще нет
    cursor.execute('CREATE TABLE IF NOT EXISTS entrys (id INTEGER PRIMARY KEY AUTOINCREMENT,sender_name TEXT,data_entry TEXT,time_entry TEXT)')

    # кладем данные в базу данных
    cursor.execute('INSERT INTO entrys (sender_name, data_entry, time_entry)VALUES (?, ?, ?)', (entry['sender_name'], entry['data_entry'], entry['time_entry']))
    conn.commit()

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data in CALLBACK_D_BUTTON:
        CALLBACK_D_BUTTON[call.data](call.message)

    #текстовое описание bpmn
    elif call.data == 'bpmn_function1':
        bot.send_message(call.message.chat.id,
                         'Диаграммы BPMN (Business Process Model and Notation) представляют собой стандартный '
                         'графический язык, разработанный для моделирования бизнес-процессов в организации. '
                         'Этот инструмент обеспечивает единый и понятный способ визуализации бизнес-процессов, '
                         'что помогает более эффективно понимать, анализировать и оптимизировать деятельность компании')

        bpmn_function_markup = types.InlineKeyboardMarkup(row_width=1)

        button11 = types.InlineKeyboardButton('Как телеграм бот может помочь в процессе '
                                              'обработки записей на мойку авто', callback_data='bpmn_function3')
        button12 = types.InlineKeyboardButton('Изображение BPMN схемы', callback_data='bpmn_function4')

        bpmn_function_markup.add(button11, button12)
        bot.send_message(call.message.chat.id, 'Выберите действие:', reply_markup=bpmn_function_markup)

    elif call.data == 'bpmn_function2':
        bot.send_message(call.message.chat.id, 'Ссылка на диаграмму: https://github.com/Pelmeshka-2848/RGR/blob/main/BPMN.jpg')
    elif call.data == 'bpmn_function3':
        bot.send_message(call.message.chat.id, 'Телеграм-бот может значительно упростить и ускорить процесс обработки записей на мойку авто. '
                                               'Вот несколько способов, как он может быть полезен:'
                                               'Установка напоминания: Клиенты могут оставлять запрос на, '
                                               'напоминание о записи. Так же это можно интегрировать вместе с приложением Google Календарь'
                                               'Интеграция с платежными системами: Для удобства клиентов бот может интегрироваться с '
                                               'платежными системами, позволяя им оплачивать услуги напрямую через телеграм.'
                                               'Обратная связь и поддержка: Клиенты могут общаться с ботом для задания вопросов, '
                                               'уточнения деталей услуги или предоставления обратной связи.')
    elif call.data == 'bpmn_function4':
        image7_url = 'https://raw.githubusercontent.com/Pelmeshka-2848/RGR/main/BPMN.jpg'
        bot.send_photo(call.message.chat.id, image7_url, caption='Это схема BPMN')

        #кнопки дашборда
    elif call.data == 'dashboard':
        dashboard_markup = types.InlineKeyboardMarkup(row_width=1)
        button1 = types.InlineKeyboardButton('Описание дашборда', callback_data='dashboard_function1')
        button2 = types.InlineKeyboardButton('Ссылка на GitHub', callback_data='dashboard_function2')
        dashboard_markup.add(button1, button2)
        bot.send_message(call.message.chat.id, 'Выберите действие:', reply_markup=dashboard_markup)
    elif call.data == 'dashboard_function1':
        bot.send_message(call.message.chat.id, 'Дашборд предназначен для визуализации и анализа данных о работе сервиса мойки авто. '
                                               'Содержит пять ключевых графиков, предоставляющих информацию о различных аспектах клиетских авто и спроса на услуги.')

        dashboard_function_markup = types.InlineKeyboardMarkup(row_width=1)

        button3 = types.InlineKeyboardButton('График 1', callback_data='dashboard_function3')
        button4 = types.InlineKeyboardButton('График 2', callback_data='dashboard_function4')
        button5 = types.InlineKeyboardButton('График 3', callback_data='dashboard_function5')
        button6 = types.InlineKeyboardButton('График 4', callback_data='dashboard_function6')
        button7 = types.InlineKeyboardButton('График 5', callback_data='dashboard_function7')
        button8 = types.InlineKeyboardButton('Таблица', callback_data='dashboard_function8')
        dashboard_function_markup.add(button3, button4, button5, button6, button7, button8)
        bot.send_message(call.message.chat.id, 'Выберите график:', reply_markup=dashboard_function_markup)

    elif call.data == 'dashboard_function2':
        bot.send_message(call.message.chat.id, 'Ссылка на GitHub: https://github.com/Pelmeshka-2848/DASHBOARD')
    elif call.data == 'dashboard_function3':
        image1_url = 'https://raw.githubusercontent.com/Pelmeshka-2848/RGR/main/image1.jpg'
        bot.send_photo(call.message.chat.id, image1_url, caption='Это точечный график')
    elif call.data == 'dashboard_function4':
        image2_url = 'https://raw.githubusercontent.com/Pelmeshka-2848/RGR/main/image2.jpg'
        bot.send_photo(call.message.chat.id, image2_url, caption='Это столбчатый график')
    elif call.data == 'dashboard_function5':
        image3_url = 'https://raw.githubusercontent.com/Pelmeshka-2848/RGR/main/image3.jpg'
        bot.send_photo(call.message.chat.id, image3_url, caption='Это круговой график')
    elif call.data == 'dashboard_function6':
        image4_url = 'https://raw.githubusercontent.com/Pelmeshka-2848/RGR/main/image4.jpg'
        bot.send_photo(call.message.chat.id, image4_url, caption='Это линейный график')
    elif call.data == 'dashboard_function7':
        image5_url = 'https://raw.githubusercontent.com/Pelmeshka-2848/RGR/main/image5.jpg'
        bot.send_photo(call.message.chat.id, image5_url, caption='Это ящичковый график')
    elif call.data == 'dashboard_function8':
        image6_url = 'https://raw.githubusercontent.com/Pelmeshka-2848/RGR/main/image6.jpg'
        bot.send_photo(call.message.chat.id, image6_url, caption='Это таблица')

bot.infinity_polling()