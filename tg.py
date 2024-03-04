import telebot
from telebot import types

# Укажите токен вашего бота
TOKEN = '6574304289:AAHbp-YuG9efM7lV--d9nOFawwGERdRZhmg'


# Создаем экземпляр бота
bot = telebot.TeleBot(TOKEN)

# Функция для отображения начального меню
def display_start_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buy_button = types.KeyboardButton("Купить")
    profile_button = types.KeyboardButton("Профиль")
    free_trial_button = types.KeyboardButton("Бесплатный тест")
    markup.add(buy_button, profile_button)
    markup.add(free_trial_button)
    bot.send_message(message.chat.id, "Привет! Я бот для продажи подписки на VPN. ", reply_markup=markup)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    display_start_menu(message)

# Обработчик команды "Профиль"
@bot.message_handler(func=lambda message: message.text == "Профиль")
def profile(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    profile_button = types.KeyboardButton("Профиль")
    markup.add(profile_button)
    bot.send_message(message.chat.id, "Ваш профиль:", reply_markup=markup)
    bot.send_message(message.chat.id, "Дополнительные опции в профиле:\nНажмите кнопку 'Информация', чтобы получить дополнительную информацию", 
                     reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True).add(types.KeyboardButton("Информация")))

# Обработчик команды "Купить"
@bot.message_handler(func=lambda message: message.text == "Купить")
def buy(message):
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