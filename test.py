import telebot
from telebot import types

# Укажите токен вашего бота
TOKEN = '6574304289:AAHbp-YuG9efM7lV--d9nOFawwGERdRZhmg'

# Создаем экземпляр бота
bot = telebot.TeleBot(TOKEN)

# Словарь для хранения состояний пользователей (стек диалогов)
user_states = {}

# Словарь для хранения id пользователей
users = {}

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    if chat_id not in users:
        users[chat_id] = {"id": chat_id}
    display_start_menu(message)

# Функция для отображения начального менюff
def display_start_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buy_button = types.KeyboardButton("Купить VPN")
    profile_button = types.KeyboardButton("Профиль")
    free_trial_button = types.KeyboardButton("Бесплатный тест")
    markup.add(buy_button, profile_button)
    markup.add(free_trial_button)
    bot.send_message(message.chat.id, "👾 Приветствую! Я Ваш личный бот и помощник MaskVPN!\n \nЯ помогаю c обходом блокировок и защитой вашей конфиденциальности.", reply_markup=markup)

# Функция для отображения профиля
def display_profile(message):
    chat_id = message.chat.id
    if chat_id not in users:
        users[chat_id] = {"id": chat_id}
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    profile_button = types.KeyboardButton("Профиль")
    markup.add(profile_button)
    bot.send_message(message.chat.id, f"Ваш профиль (ID: {users[chat_id]['id']}):", reply_markup=markup)
    bot.send_message(message.chat.id, "Дополнительные опции в профиле:", 
                     reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("Информация", callback_data="info")))
    # Отправляем кнопки Купить и Бесплатный тест
    display_start_menu(message)

# Обработчик команды "Профиль"
@bot.message_handler(func=lambda message: message.text == "Профиль")
def profile(message):
    display_profile(message)



# Обработчик команды "Купить"
@bot.message_handler(func=lambda message: message.text == "Купить VPN")
def buy(message):
    markup = types.InlineKeyboardMarkup()

    tariffs = [
        {"months": 1, "price": 250},
        {"months": 3, "price": 600},
        {"months": 6, "price": 1000},
        {"months": 12, "price": 1800}
    ]

    for tariff in tariffs:
        button_text = f"{tariff['months']} месяц{'а' if tariff['months'] != 1 else ''}\n{tariff['price']} ₽"
        button = types.InlineKeyboardButton(button_text, callback_data=f"buy_{tariff['months']}_{tariff['price']}")
        markup.add(button)
    bot.send_message(message.chat.id, "Выберите удобный для вас тариф: \n\n\n\nК оплате принимаются карты РФ: Visa, MasterCard, МИР." , reply_markup=markup, parse_mode='HTML')

# Обработчик нажатия на кнопки способов оплаты и тарифов
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    chat_id = call.message.chat.id
    user_id = call.from_user.id

    # Обработка нажатия на кнопку выбора тарифа
    if call.data.startswith('buy_'):
        data = call.data.split('_')
        if len(data) == 3:
            months = int(data[1])
            price = int(data[2])
       
            # Создаем кнопки для способов оплаты
            payment_markup = types.InlineKeyboardMarkup(row_width=4)
            payment_markup.add(types.InlineKeyboardButton("Банковская карта", callback_data=f"payment_card_{months}_{price}"),
                               types.InlineKeyboardButton("BTC", callback_data=f"payment_btc_{months}_{price}"),
                               types.InlineKeyboardButton("Назад", callback_data=f"back"))
            bot.send_message(chat_id, f"Вы выбрали тариф на <b>{months}</b> месяц{'а' if months == 1 else 'ев'}.\nСтоимость - <b>{price} рублей</b>.\n\nВыберите способ оплаты:", reply_markup=payment_markup, parse_mode='HTML')

    # Обработка нажатия на кнопки способов оплаты
    elif call.data.startswith('payment_'):
        data = call.data.split('_')
        if len(data) == 4:
            payment_method = data[1]
            months = int(data[2])
            price = int(data[3])
            if payment_method == "card":
                # Ваша логика для оплаты банковской картой
                bot.send_message(chat_id, f"Покупка на {months} месяцев успешно совершена! Оплачено банковской картой.")
            elif payment_method == "btc":
                # Ваша логика для оплаты через BTC
                bot.send_message(chat_id, f"Покупка на {months} месяцев успешно совершена! Оплачено через BTC.")

            # Обработка нажатия кнопки "Назад"
            elif call.data == "back":
                buy(call.message)
                
# Обработчик команды "Бесплатный тест"
@bot.message_handler(func=lambda message: message.text == "Бесплатный тест")
def free_trial(message):
    # Здесь можно добавить логику для предоставления бесплатного теста
    bot.reply_to(message, "Вы выбрали Бесплатный тест. Наслаждайтесь бесплатным тестом VPN!")

# Запускаем бота
bot.polling()