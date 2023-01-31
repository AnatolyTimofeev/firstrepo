import telebot
from config import keys , TOKEN
from utils import ConvertionExeption , CryptoConverter




bot = telebot.TeleBot(TOKEN)
@bot.message_handler(commands= ['start', 'help'])
def echo_test(message: telebot.types.Message):
    text = 'Чтобы начать работу введите имя команды в формате через пробел : \n имя валюты  \
в какую валюту перевести \
сумма \n например :\n евро рубль 100 \n \
можно увидеть список всех доступных валют через команду /values'
    bot.send_message(message.chat.id , text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'доступные валюты'
    for key in keys.keys():
       text = '\n'.join((text, key ,))
    bot.reply_to(message, text)
@bot.message_handler(content_types=['text',])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionExeption('слишком много(мало) параметров')
        quote , base , amount = values

        total_base = CryptoConverter.get_price(quote , base , amount)
        total_ = round(float(total_base)*float(amount) , 2)
    except ConvertionExeption as e:
        bot.reply_to(message , f'Ошибка полльзователя {e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду {e}')
    else:
        text = f'Цена  {amount} {quote} в {base} = {total_}'
        bot.send_message(message.chat.id , text)

bot.polling(none_stop=True)