import telebot
from config import keys, TOKEN
from extensions import ConvertinException, CryptoConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = "Чтобы начать работу введите команду боту в следующем формате: \n<Имя валюты(рубль/евро/доллар)> \
<В какую валюту перевести> \
<количество переводимой валюты> \nУвидеть список доступных валют: /values"
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def value(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertinException('Слишком много параметров.')

        quote, base, amount = values
        total_base = CryptoConverter.convert(quote, base, amount)
    except ConvertinException as e:
        bot.reply_to(message, f'Ошибка пользователяю\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)

bot.polling(none_stop=True, interval=0)