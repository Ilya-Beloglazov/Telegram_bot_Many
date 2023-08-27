import telebot
from currency_converter import CurrencyConverter
from telebot import types



bot=telebot.TeleBot('6540357667:AAHmelC0W94mvyYXv24pbs-KPCkhgK6Es9Q')
currency=CurrencyConverter()
amount=0



@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id,'Здравствуйте, вот как пользоваться этим ботом : 1. отправьте команду /start, \n'
                                     'затем введите число , а потом выберите валюты ')


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,'Здравствуйте , введите сумму : ')
    bot.register_next_step_handler(message,summa)


def summa(message):
    global amount
    try:
        amount = int(message.text.strip())
    except ValueError:
        bot.send_message(message.chat.id, 'Неверный формат , мне нужны положительные числа =)')
        bot.register_next_step_handler(message,summa)
        return

    if amount>0:

        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton('USD/EUR',callback_data='usd/eur')
        btn2 = types.InlineKeyboardButton('EUR/USD', callback_data='eur/usd')
        btn3 = types.InlineKeyboardButton('USD/RUB', callback_data='usd/rub')
        btn4 = types.InlineKeyboardButton('Другое значение', callback_data='else')
        markup.add(btn1,btn2,btn3,btn4)
        bot.send_message(message.chat.id,'Выберите пару валют',reply_markup=markup)
    else:
        bot.send_message(message.chat.id,'Число должно быть больше чем 0. Впишите сумму ')
        bot.register_next_step_handler(message,summa)



@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data !='else':
        values = call.data.upper().split('/')
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(call.message.chat.id, f'Выходит:{round(res,2)}/ Вы можете заново вписать сумму :')
        bot.register_next_step_handler(call.message, summa)
    else:
        bot.send_message(call.message.chat.id,'Введите пару значений через слэш')
        bot.register_next_step_handler(call.message, mycurrency)

def my_currency(message):
    try:
        values=message.text.upper().split('/')
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(message.chat.id, f'Выходит:{round(res, 2)}/ Вы можете заново вписать сумму :')
        bot.register_next_step_handler(message, summa)
    except Exception:
        bot.send_message(message.chat.id, f'Что-то пошло не так , повторите попытку')
        bot.register_next_step_handler(message, summa)








bot.polling(none_stop=True)

