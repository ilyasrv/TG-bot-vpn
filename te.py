import telebot
from telebot import types


# Укажите токен вашего бота
TOKEN = '6574304289:AAHbp-YuG9efM7lV--d9nOFawwGERdRZhmg'

# Set your YooMoney API keys
YMONEY_SHOP_ID = '59794627D5DD9B90D96B924297FD2C8764FE24D03C9A833B34B2CE6B49EB13C0'
YMONEY_SECRET_KEY = "4100117853537949.83A3FB772A51B28DB1A367CE946AB11E68E3EEEBC7AD86C0601BAFFBC739F0DC051674F31EDC39F79BECE6E2154D205E1A3FB3B936A3A0BF44BCB06A68C277217CE82BEEB90DB947763D5F43B411CB9C1A8638260B0B995AE0C2D0555AF21F19518DB340ED7B3F1CF240763CAA7ACD7FF6D3B317F578AB39F9B4F4C89C5F0E8C"
# Создаем экземпляр бота
bot = telebot.TeleBot(TOKEN)

# Словарь для хранения id пользователей
users = {}
PRICES = {
    1: 2,
    3: 840,
    6: 1500,
    12: 2000
}
# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    if chat_id not in users:
        users[chat_id] = {"id": chat_id}
    display_start_menu(message)

# Функция для отображения начального меню
def display_start_menu(message, show_welcome=True):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buy_button = types.KeyboardButton("Купить")
    profile_button = types.KeyboardButton("Профиль")
    get_key_button = types.KeyboardButton("Получить ключ")
    free_trial_button = types.KeyboardButton("Бесплатный тест")
    markup.add(buy_button, profile_button, get_key_button)
    markup.add(free_trial_button)
    if show_welcome:
        bot.send_message(message.chat.id, "Привет! Я бот для продажи подписки на VPN.", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "Выберите действие:", reply_markup=markup)

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
# Обработчик нажатия на инлайн-кнопки для покупки
@bot.callback_query_handler(func=lambda call: call.data.startswith('buy_'))
def process_buying(call):
    chat_id = call.message.chat.id
    user_id = call.from_user.id

    duration = int(call.data.split('_')[1])
    price = PRICES.get(duration)
    if price is None:
        bot.send_message(chat_id, "Не удалось определить цену. Попробуйте еще раз.")
        return

    try:
        # Создание платежа с использованием YooMoney
        from yoomoney import Quickpay
        quickpay = Quickpay(
            receiver="4100117853537949",
            quickpay_form="shop",
            targets="Sponsor this project",
            paymentType="SB",
            sum=price,    
            label="a1b2c3d4e5"
            )
        print(quickpay.base_url)
        print(quickpay.redirected_url)  
        from yoomoney import Client
        token = YMONEY_SECRET_KEY
        client = Client(token)
        history = client.operation_history(label="a1b2c3d4e5")
        print("List of operations:")
        print("Next page starts with: ", history.next_record)
        for operation in history.operations:
            print()
        print("Operation:",operation.operation_id)
        print("\tStatus     -->", operation.status)
        print("\tDatetime   -->", operation.datetime)
        print("\tTitle      -->", operation.title)
        print("\tPattern id -->", operation.pattern_id)
        print("\tDirection  -->", operation.direction)
        print("\tAmount     -->", operation.amount)
        print("\tLabel      -->", operation.label)
        print("\tType       -->", operation.type)
        if operation.status == "success":
            handle_successful_payment(user_id, duration)
        else:
            bot.send_message(chat_id, "Оплата не была завершена. Попробуйте еще раз или обратитесь в поддержку.")
        # Отправка сообщения с инструкциями по оплате
        bot.send_message(chat_id, f"Чтобы завершить покупку, перейдите по ссылке и выполните оплату:{quickpay.base_url}")

    except Exception as e:
        # Ошибка при создании платежа
        bot.send_message(chat_id, f"Произошла ошибка при обработке платежа: {e}")

# Обработка успешного платежа
def handle_successful_payment(user_id, duration):
    # Обновление записей пользователя или предоставление доступа к услуге после успешной оплаты
    bot.send_message(user_id, f"Поздравляем! Вы успешно приобрели подписку на VPN на {duration} месяц{'а' if duration > 1 else ''}.")

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

# Обработчик команды "Получить ключ"
@bot.message_handler(func=lambda message: message.text == "Получить ключ")
def get_key(message):
    # Implement the logic to generate and provide a key to the user
    # For example, you can generate a random key and send it to the user
    key = generate_random_key()
    bot.send_message(message.chat.id, f"Ваш ключ: {key}")

def generate_random_key():
    # Implement your logic to generate a random key
    # For example, you can use Python's uuid module to generate a UUID
    import uuid
    return str(uuid.uuid4())

# Генерирует и отправляет сообщение приветствия и клавиатуру
    display_start_menu(message)

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


