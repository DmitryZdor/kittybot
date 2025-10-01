import logging
import os
import requests
from dotenv import load_dotenv
from telegram.ext import CommandHandler, Updater
from telegram import ReplyKeyboardMarkup

load_dotenv()

secret_token = os.getenv('TOKEN')

URL_DOG = 'https://api.thecdogapi.com/v1/images/search'

DATA = {
    '/cat': ('https://api.thecatapi.com/v1/images/search', 0),
    '/fox': ('https://randomfox.ca/floof/', 1),
    '/dog': ('https://random.dog/woof.json', 2),
    '/capy': ('https://api.capy.lol/v1/capybara?json=true', 3),
}

menu = list(DATA.keys())

def get_new_image(animal):
    try:
        response = requests.get(DATA[animal][0])
    except Exception as error:
        # print(error)
        logging.error(f'Ошибка при запросе к основному API: {error}')
        response = requests.get(URL_DOG)
        response = response.json()
        return response[0].get('url')

    response = response.json()
    print(response)
    idx = DATA[animal][1]
    if idx == 0:
        return response[0].get('url')
    elif idx == 1:
        return response["link"]
    elif idx == 2:
        return response["url"]
    elif idx == 3:
        return response["data"]["url"]


def new(update, context):
    animal = update.message.text
    print(animal)
    chat = update.effective_chat
    name = update.message.chat.first_name
    button = ReplyKeyboardMarkup([DATA], resize_keyboard=True)
    context.bot.send_message(
        chat_id=chat.id,
        text=f'Привет, {name}. Посмотри, какого красавчика я тебе нашел на просторах интернета!',
        reply_markup=button
    )

    context.bot.send_photo(chat.id, get_new_image(animal))


def wake_up(update, context):
    # В ответ на команду /start
    # будет отправлено сообщение 'Спасибо, что включили меня'
    chat = update.effective_chat
    name = update.message.chat.first_name

    button = ReplyKeyboardMarkup([DATA], resize_keyboard=True)
    context.bot.send_message(
        chat_id=chat.id,
        text=f'Спасибо {name}, что включили меня\n'
             f'выбирайте кого вам прислать',
        reply_markup=button
    )


def main():
    updater = Updater(token=secret_token)
    # Регистрируется обработчик CommandHandler;
    # он будет отфильтровывать только сообщения с содержимым '/start'
    # и передавать их в функцию wake_up()
    updater.dispatcher.add_handler(CommandHandler('start', wake_up))
    updater.dispatcher.add_handler(CommandHandler('cat', new))
    updater.dispatcher.add_handler(CommandHandler('capy', new))
    updater.dispatcher.add_handler(CommandHandler('fox', new))
    updater.dispatcher.add_handler(CommandHandler('dog', new))
    # Метод start_polling() запускает процесс polling,
    # приложение начнёт отправлять регулярные запросы для получения обновлений.
    updater.start_polling()
    # Бот будет работать до тех пор, пока не нажмете Ctrl-C
    updater.idle()


if __name__ == '__main__':
    main()
