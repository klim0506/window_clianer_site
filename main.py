import telebot
from telebot import types
import datetime

TOKEN = '5562458962:AAFV_yHHe-nf57dDlNT-VzogS3Urx2KffFs'

bot = telebot.TeleBot(TOKEN)

data = {}
order_dates = ["22.07", "23.07", "24.07", "25.07", "26.07", "27.07", "28.07", "29.07", "31.07",
               "1.08", "2.08", "3.08", "4.08", "5.08", "6.08", "7.08"]

order_time = {'22.07': ['9:00', '11:30', '14:00', '16:30'],
              '23.07': ['9:00', '11:30', '14:00', '16:30', '19:00'],
              '24.07': ['9:00', '11:30', '14:00', '16:30', '19:00'],
              '25.07': ['16:30'],
              '26.07': ['16:30', '19:00'],
              '27.07': ['16:30'],
              '28.07': ['16:30', '19:00'],
              '29.07': ['16:30'],
              '31.07': ['9:00', '11:30', '14:00', '16:30', '19:00'],
              '1.08': ['9:00', '11:30', '14:00', '16:30'],
              '2.08': ['9:00', '11:30', '14:00', '16:30', '19:00'],
              '3.08': ['9:00', '11:30', '14:00', '16:30'],
              '4.08': ['9:00', '11:30', '14:00', '16:30', '19:00'],
              '5.08': ['9:00', '11:30', '14:00', '16:30'],
              '6.08': ['9:00', '11:30', '14:00', '16:30', '19:00'],
              '7.08': ['9:00', '11:30', '14:00', '16:30', '19:00'],
              }


@bot.message_handler(commands=['start'])
def start_msg(msg):
    bot.send_message(msg.chat.id, "Здравствуйте!)")
    btn_tadle = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Заказать')
    item3 = types.KeyboardButton('Инструкция')
    item2 = types.KeyboardButton('Цены')
    item5 = types.KeyboardButton('Помощь')
    btn_tadle.add(item1, item2)
    btn_tadle.add(item3, item5)
    bot.send_message(msg.chat.id, 'Выберите что вам нужно', reply_markup=btn_tadle)


@bot.message_handler(content_types=['contact'])
def contact(msg):
    data[msg.chat.id]['phone_number'] = msg.contact.phone_number
    data[msg.chat.id]['name'] = msg.contact.first_name
    print(data)
    order_time[data[msg.chat.id]['date']].pop(order_time[data[msg.chat.id]['date']].index(data[msg.chat.id]['chosen_time'].split()[1]))
    print(order_time)
    bot.send_message(msg.chat.id, 'Спасибо за заказ!')
    bot.send_message(msg.chat.id, 'Скоро мы свяжемся с вами для подтверждения заказа')
    bot.send_message('1268418032', f"Адрес: {data[msg.chat.id]['tower']} башня, {data[msg.chat.id]['floor']} этаж, "
                                   f"квартира {data[msg.chat.id]['float']} \n"
                                   f"Время исполнения: {data[msg.chat.id]['date']} {data[msg.chat.id]['chosen_time']} \n"
                                   f"В квартире {data[msg.chat.id]['windows']} окон\n"
                                   f"_________________________________________________\n"
                                   f"Сумма заказа: {data[msg.chat.id]['price']} \n"
                                   f"Время исполнения заказа: {data[msg.chat.id]['time']} \n"
                                   f"Номер телефона: {data[msg.chat.id]['phone_number']} \n"
                                   f"id {msg.chat.id}\n"
                                   f"Имя {msg.contact.first_name}")
    end(msg)


def order(msg):
    bot.send_message(msg.chat.id, 'Что вас интересует?')


def windows(msg):
    data[msg.chat.id] = {}
    now = datetime.datetime.now()
    data[msg.chat.id]['ordered_time'] = f'{now.day}.{now.month}.{now.year} {now.hour}:{now.minute}'
    print(data)
    btn_table = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('1 окно - 2500₽')
    item2 = types.KeyboardButton('2 окна - 5000₽')
    item3 = types.KeyboardButton('3 окна - 6000₽')
    item4 = types.KeyboardButton('4 окна - 8000₽')
    item5 = types.KeyboardButton('5 окон - 10000₽')
    item6 = types.KeyboardButton('6 окон - 12000₽')
    item7 = types.KeyboardButton('7 окон - 14000₽')
    item8 = types.KeyboardButton('8+ окон - 2000₽ за каждое окно')
    btn_table.add(item1, item2, item3)
    btn_table.add(item4, item5, item6)
    btn_table.add(item7, item8)
    bot.send_message(msg.chat.id, 'Выберите сколько у вас окон', reply_markup=btn_table)


def tower(msg):
    btn_table = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Западная')
    item2 = types.KeyboardButton('Восточная')
    item3 = types.KeyboardButton('Центральная')
    btn_table.add(*[item1, item3, item2])
    bot.send_message(msg.chat.id, 'Выберите вашу башню', reply_markup=btn_table)


def floor(msg):
    btn_table = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    help_items = []
    count = 0
    for i in range(1, 45):
        if count == 4:
            count = 0
            btn_table.row(*help_items)
            help_items = []
        help_items.append(types.KeyboardButton(f'{i} этаж'))
        count += 1
    btn_table.row(*help_items)

    bot.send_message(msg.chat.id, 'Выберите ваш этаж', reply_markup=btn_table)


def date_choose(msg):
    btn_table = types.ReplyKeyboardMarkup(resize_keyboard=True)
    count = 0
    help_items = []
    day = datetime.date.today().day
    month = datetime.date.today().month
    date_index = 0
    for i in range(len(order_dates)):
        if int(order_dates[i].split('.')[0]) > day:
            date_index = i
            break

    for i in order_dates[date_index:date_index + 8]:
        if count == 4:
            count = 0
            btn_table.row(*help_items)
            help_items = []
        help_items.append(i)
        count += 1
    btn_table.row(*help_items)

    bot.send_message(msg.chat.id, 'Выберите дату', reply_markup=btn_table)


def time_choose(msg, date):
    btn_table = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if not order_time[date]:
        bot.send_message(msg.chat.id, 'К сожалению, на эту дату нет свободного времени, выберите другую дату')
    else:
        btn_table.add('🔙', *[f'c {i}' for i in order_time[date]])
        bot.send_message(msg.chat.id, f'Дата исполнения: {date}')
        bot.send_message(msg.chat.id, 'Выберите время', reply_markup=btn_table)


def confirm(msg):
    btn_table = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Всё верно. Оставить номер телефона и заказать!', request_contact=True)
    item2 = types.KeyboardButton('Начать заново')
    btn_table.add(item1)
    btn_table.add(item2)
    time = ''
    if data[msg.chat.id]['windows'] in ('1', '3'):
        time = '~1 час 30 минут'
    else:
        time = '~2 часа 30 минут'

    data[msg.chat.id]['time'] = time
    bot.send_message(msg.chat.id, 'До заказа остался один шаг - проверка данных \n'
                                  'Если все верно, нажмите кнопку "Всё верно. Оставить номер телефона и заказать!" \n'
                                  'Если вы нашли ошибку, нажмите кнопку "Начать заново"', reply_markup=btn_table)
    try:
        bot.send_message(msg.chat.id, f"Адрес: {data[msg.chat.id]['tower']} башня, {data[msg.chat.id]['floor']} этаж, "
                                      f"квартира {data[msg.chat.id]['float']} \n"
                                      f"Время исполнения: {data[msg.chat.id]['date']} {data[msg.chat.id]['chosen_time']} \n"
                                      f"В квартире {data[msg.chat.id]['windows']} окон\n"
                                      f"_________________________________________________\n"
                                      f"Сумма заказа: {data[msg.chat.id]['price']} \n"
                                      f"Время исполнения заказа: {data[msg.chat.id]['time']}")

    except Exception:
        bot.send_message(msg.chat.id, "Произошла непредвиденная ошибка, возможно, вы не использовали кнопки для выбора "
                                      "вариантов ответа. Давайте попробуем ещё раз")

    bot.send_message(msg.chat.id, 'Всё верно?', reply_markup=btn_table)


def end(msg):
    btn_tadle = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Заказать')
    item3 = types.KeyboardButton('Инструкция')
    item2 = types.KeyboardButton('Цены')
    item5 = types.KeyboardButton('Помощь')
    btn_tadle.add(item1, item2)
    btn_tadle.add(item3, item5)
    bot.send_message(msg.chat.id, 'Если остались вопросы, то обратиться в поддержку можно в раздеде "Помощь"', reply_markup=btn_tadle)


@bot.message_handler(content_types='text')
def message_reply(msg):
    if msg.text == "Заказать":
        windows(msg)

    elif msg.text == "Помощь":
        bot.send_message(msg.chat.id, "Не нашли ответа на ваш вопрос? \n\n"
                                      "Напишите ваш вопрос сообщением ниже и скоро мы на него ответим")

    elif msg.text == "Цены":
        bot.send_message(msg.chat.id, """❓Сколько стоит помыть окна?

1-2 окна - 2500 руб/окно
3+ окон - 2000 руб/окно

Мойка окон выполняется с внешней стороны при помощи вакуумных роботов.

Уборка занимает от 1 до 2,5 часов, в зависимости от количества окон. Ориентировочная длительность будет указана после заполнения всех полей заказа: перед подтверждением. 

Для бронирования мойки нажмите на кнопку "заказать" и ответьте на все вопросы""")

    elif msg.text == "Инструкция":
        bot.send_message(msg.chat.id,
                         """❓Как заказать мойку?

1. Нажмите на кнопку "Заказать"
2. Выберите сколько окон нужно помыть
3. Выберите башню 
4. Выберите этаж
5. Введите номер квартиры
6. Выберите удобную дату
7. Выберите время (если на эту дату нет удобного времени, то нажмите кнопку "back" и выберите другую дату)
8. Подтвердите данные""")

    elif msg.text == '1 окно - 2500₽':
        data[msg.chat.id]['price'] = '2500 рублей'
        data[msg.chat.id]['windows'] = '1'
        tower(msg)
        print(data)

    elif msg.text == '2 окна - 5000₽':
        data[msg.chat.id]['price'] = '5000 рублей'
        data[msg.chat.id]['windows'] = '2'
        tower(msg)
        print(data)

    elif msg.text == '3 окна - 6000₽':
        data[msg.chat.id]['price'] = '6000 рублей'
        data[msg.chat.id]['windows'] = '3'
        tower(msg)
        print(data)

    elif msg.text == '4 окна - 8000₽':
        data[msg.chat.id]['price'] = '8000 рублей'
        data[msg.chat.id]['windows'] = '4'
        tower(msg)
        print(data)

    elif msg.text == '5 окон - 10000₽':
        data[msg.chat.id]['price'] = '10000 рублей'
        data[msg.chat.id]['windows'] = '5'
        tower(msg)
        print(data)

    elif msg.text == '6 окон - 12000₽':
        data[msg.chat.id]['price'] = '12000 рублей'
        data[msg.chat.id]['windows'] = '6'
        tower(msg)
        print(data)

    elif msg.text == '7 окон - 14000₽':
        data[msg.chat.id]['price'] = '14000 рублей'
        data[msg.chat.id]['windows'] = '7'
        tower(msg)
        print(data)

    elif msg.text == '8+ окон - 2000₽ за каждое окно':
        data[msg.chat.id]['price'] = '2000 рублей за окно'
        data[msg.chat.id]['windows'] = '8+'
        tower(msg)
        print(data)

    elif msg.text == 'Западная':
        data[msg.chat.id]['tower'] = 'Западная'
        floor(msg)
        print(data)

    elif msg.text == 'Восточная':
        data[msg.chat.id]['tower'] = 'Восточная'
        floor(msg)
        print(data)

    elif msg.text == 'Центральная':
        data[msg.chat.id]['tower'] = 'Центральная'
        floor(msg)
        print(data)

    elif 'этаж' in msg.text:
        data[msg.chat.id]['floor'] = msg.text.split()[0]
        bot.send_message(msg.chat.id, 'Введите номер вашей квартиры')
        print(data)

    elif msg.text.isnumeric():
        print(msg.text)
        data[msg.chat.id]['float'] = msg.text
        date_choose(msg)
        print(data)

    elif msg.text.split('.')[0].isnumeric():
        date = msg.text
        data[msg.chat.id]['date'] = date
        time_choose(msg, date)
        print(data)

    elif msg.text == '🔙':
        date_choose(msg)

    elif ':' in msg.text:
        data[msg.chat.id]['chosen_time'] = msg.text
        confirm(msg)
        print(data)

    elif msg.text == 'Начать заново':
        start_msg(msg)

    else:
        print(f"\nНеизвестное сообщение от {msg.chat.username}  ------------  {msg.text}\n")


bot.infinity_polling()
