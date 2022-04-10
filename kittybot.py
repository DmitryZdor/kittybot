import logging
import os
import requests
from dotenv import load_dotenv
from telegram.ext import CommandHandler, Updater
from telegram import ReplyKeyboardMarkup

load_dotenv()

secret_token = os.getenv('TOKEN')


URL = 'https://api.thecatapi.com/v1/images/search'


def get_new_image():
    try:
        response = requests.get(URL)
    except Exception as error:
        #print(error)
        logging.error(f'Ошибка при запросе к основному API: {error}')
        new_url = 'https://api.thedogapi.com/v1/images/search'
        response = requests.get(new_url)

    response = response.json()
    random_cat = response[0].get('url')
    return random_cat


def new_cat(update, context):
    chat = update.effective_chat
    context.bot.send_photo(chat.id, get_new_image())


def wake_up(update, context):
    # В ответ на команду /start
    # будет отправлено сообщение 'Спасибо, что включили меня'
    chat = update.effective_chat
    name = update.message.chat.first_name

    button = ReplyKeyboardMarkup([['/newcat']], resize_keyboard=True)
    context.bot.send_message(
        chat_id=chat.id,
        text='Привет, {}. Посмотри, какого котика я тебе нашёл'.format(name),
        reply_markup=button
    )

    context.bot.send_photo(chat.id, get_new_image())


def main():
    updater = Updater(token=secret_token)
    # Регистрируется обработчик CommandHandler;
    # он будет отфильтровывать только сообщения с содержимым '/start'
    # и передавать их в функцию wake_up()
    updater.dispatcher.add_handler(CommandHandler('start', wake_up))
    updater.dispatcher.add_handler(CommandHandler('newcat', new_cat))

    # Метод start_polling() запускает процесс polling,
    # приложение начнёт отправлять регулярные запросы для получения обновлений.
    updater.start_polling()
    # Бот будет работать до тех пор, пока не нажмете Ctrl-C
    updater.idle()


if __name__ == '__main__':
    main()
