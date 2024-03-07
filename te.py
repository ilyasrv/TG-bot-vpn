import telebot
from telebot import types

# Укажите токен вашего бота
TOKEN = '6574304289:AAHbp-YuG9efM7lV--d9nOFawwGERdRZhmg'

# Создаем экземпляр бота
bot = telebot.TeleBot(TOKEN)

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
    buy_button = types.KeyboardButton("Купить")
    profile_button = types.KeyboardButton("Профиль")
    free_trial_button = types.KeyboardButton("Бесплатный тест")
    markup.add(buy_button, profile_button)
    markup.add(free_trial_button)
    bot.send_message(message.chat.id, "Привет! Я бот для продажи подписки на VPN.", reply_markup=markup)

# Функция для отображения профиля
def display_profile(message):
    chat_id = message.chat.id
    if chat_id not in users:
        users[chat_id] = {"id": chat_id}
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    profile_button = types.KeyboardButton("Профиль")
    markup.add(profile_button)
    bot.send_message(message.chat.id, f"Ваш профиль (ID: {users[chat_id]['id']}):", reply_markup=markup)
    
    # Создаем inline клавиатуру для дополнительных опций
    additional_markup = types.InlineKeyboardMarkup()
    additional_markup.row(types.InlineKeyboardButton("Информация", callback_data="info"))
    additional_markup.row(types.InlineKeyboardButton("Мои ключи", callback_data="my_keys"))  # Add the "My Keys" button
                          
    bot.send_message(message.chat.id, "Дополнительные опции в профиле:", reply_markup=additional_markup)
    # Отправляем кнопки Купить и Бесплатный тест
    display_start_menu(message) 
# Обработчик команды "Профиль"
@bot.message_handler(func=lambda message: message.text == "Профиль")
def profile(message):
    display_profile(message)

# Обработчик команды "Купить"
@bot.message_handler(func=lambda message: message.text == "Купить")
def buy(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    button1 = types.InlineKeyboardButton("1 месяц - 350p", callback_data='buy_1_month')
    button3 = types.InlineKeyboardButton("3 месяца - 840p", callback_data='buy_3_months')
    button6 = types.InlineKeyboardButton("6 месяцев - 1500p", callback_data='buy_6_months')
    button12 = types.InlineKeyboardButton("12 месяцев - 2000p", callback_data='buy_12_months')
    markup.add(button1, button3, button6, button12)

    bot.send_message(message.chat.id, "Выберите тариф:", reply_markup=markup)

# Обработчик команды "Бесплатный тест"
@bot.message_handler(func=lambda message: message.text == "Бесплатный тест")
def free_trial(message):
    # Здесь можно добавить логику для предоставления бесплатного теста
    bot.reply_to(message, "Вы выбрали Бесплатный тест. Наслаждайтесь бесплатным тестом VPN!")

# Обработчик нажатия на инлайн-кнопки
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    chat_id = call.message.chat.id
    user_id = call.from_user.id

    if call.data.startswith('buy_'):
        months = int(call.data.split('_')[1])
        # Здесь можно добавить логику для обработки покупки в зависимости от выбранного периода подписки
        bot.send_message(chat_id, f"Вы выбрали тариф на {months} месяцев. Стоимость - {months * 10}$.")

    elif call.data == "info":
        # Здесь можно добавить логику для обработки нажатия на кнопку "Информация"
        bot.send_message(chat_id, "Здесь будет информация о нашем сервисе VPN.")

# Запускаем бота
bot.polling()