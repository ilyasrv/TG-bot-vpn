import telebot
from telebot import types


# Укажите токен вашего бота
TOKEN = '6574304289:AAHbp-YuG9efM7lV--d9nOFawwGERdRZhmg'
users = {}

# Создаем экземпляр бота
bot = telebot.TeleBot(TOKEN)

# Функция для отображения начального меню
def display_start_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buy_button = types.KeyboardButton("Купить VPN")
    profile_button = types.KeyboardButton("Профиль")
    free_trial_button = types.KeyboardButton("Бесплатный тест")
    markup.add(buy_button, profile_button)
    markup.add(free_trial_button)
    bot.send_message(message.chat.id, "👾 Приветствую! Я Ваш личный бот и помощник MaskVPN!\n \nЯ помогаю c обходом блокировок и защитой вашей конфиденциальности.", reply_markup=markup)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    display_start_menu(message)

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
@bot.message_handler(func=lambda message: message.text == "Купить")
def buy(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    month_button = types.KeyboardButton("1 месяц (100 руб.)")
    three_months_button = types.KeyboardButton("3 месяца (250 руб.)")
    six_months_button = types.KeyboardButton("6 месяцев (450 руб.)")
    twelve_months_button = types.KeyboardButton("12 месяцев (800 руб.)")
    back_button = types.KeyboardButton("Назад")
    markup.add(month_button, three_months_button)
    markup.add(six_months_button, twelve_months_button)
    markup.add(back_button)
    bot.send_message(message.chat.id, "Выберите тариф:", reply_markup=markup)

    # Здесь можно добавить логику для покупки подписки
    bot.reply_to(message, "Вы выбрали Купить. Покупайте подписку на VPN здесь.")

# Обработчик команды "Информация"
@bot.message_handler(func=lambda message: message.text == "Информация")
def information(message):
    # Здесь можно добавить информацию о вашем сервисе VPN
    bot.reply_to(message, "Вы выбрали Информация. Здесь будет информация о нашем сервисе VPN.")

# Обработчик команды "Бесплатный тест"
@bot.message_handler(func=lambda message: message.text == "Бесплатный тест")
def free_trial(message):
    # Здесь можно добавить логику для предоставления бесплатного теста
    bot.reply_to(message, "Вы выбрали Бесплатный тест. Наслаждайтесь бесплатным тестом VPN!")

# Запускаем бота
bot.polling()