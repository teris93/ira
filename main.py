import telebot  # импорт библиотеки, отвечающая за функционал телеграм бота
import utils  # импорт класса исключений
import consts


bot = telebot.TeleBot(consts.TOKEN)  # инициализации бота в python'e


@bot.message_handler(commands=['start', 'help'])  # реагирование бота на команды start & help
def command_start_help(message: telebot.types.Message):  # относится ли message типу класса Message
    text = ('Чтобы начать работу введите комманду боту в следующем формате:'
            '\n <имя валюты, цену которой вы хотите узнать> '
            '<имя валюты, в которой надо узнать цену первой валюты> '
            '<цена валюты>.'
            '\nУвидеть список всех доступных валют: /values.')
    bot.reply_to(message, text)  # reply_to выделяет последнее сообщение пользователя и отвечает на него с ссылкой


@bot.message_handler(commands=['values'])  # реагирование бота на команду values
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for counter, key in enumerate(consts.keys.keys(), 1):
        text += f'\n{counter}) {key}'  # перечисление элементов словаря keys, который вызывается через импорт

    bot.reply_to(message, text)


@bot.message_handler(commands=['stop'])  # так как я бота тестировал в группе не из двух человек, бот реагировал на все
# сообщения, что бы как то тормозить бота в его реализации использовал данную команду
def strop_bot(message: telebot.types.Message):
    bot.send_message(message.chat.id, 'Выключение бота!!!')  # send_message, команда, которая говорит о том,
# что бот будет отправлять сообщение, важно знать id чата, в котором бот исопльзуется
    bot.stop_polling()  # завершение работы бота


@bot.message_handler(content_types=['text'])  # реагирование бота на текстовые сообщения от пользователей
# ВАЖНО: если бот используется в группе из двух и более человек, бот должен владеть правами администратора в группе
# что бы он мог отправлять сообщения в группе, иначе он будет реагировать только на commands, такие как start, help...
def convert(message: telebot.types.Message):
    try:  # отлавливание ошибки конструкцией tre-except-else
        correct_message = message.text.lower().split()  # регистрочувствительный ввод
        joke_message = message.text.split()  # так как бот тестировался в группе,
        # наверное мне было важно сделать вывод таким, каким был ввод

        if len(correct_message) != 3:  # проверка на наличия количества элементов в списке
            raise utils.APIException('Неверно указан формат ввода, формат ввода должен соответствовать условию:'
                                     '\n <имя валюты, цену которой вы хотите узнать> '
                                     '<имя валюты, в которой надо узнать цену первой валюты> '
                                     '<цена валюты>.')

        quote, base, amount = correct_message  # разделение списка на 3 переменные, отвечающие за корректный вывод
        utils.CryptoConverter.exceptions(quote, base, amount)  # вызов класса с ошибками
        # сначала идет проверка на ошибки потом все остальное

    except utils.APIException as exc:  # если ошибка относится к известным ошибкам, будет срабатывать нужное исключение
        bot.reply_to(message, f'Ошибка пользователя: {exc}')
    except Exception as exc:  # если ошибка не относится к известной, будет вызываться системная ошибка (исключение)
        bot.reply_to(message, f'Системная ошибка: {exc}')

    else:
        total = utils.Price.get_price(quote, base, amount)  # вызов статического метода класса Price
        # отвечающий за вывод цены валюты
        text = f'Цена {amount} {joke_message[0]} в {joke_message[1]} - {total}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)  # запуск бота с функцией без остановочного режима, который игнорирует ошибки.
