import telebot
from settings import TOKEN
from model import get_class
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def welcome(message):
    if message.text == '/start':
        welcome_text= 'Привет! Я бот, который может различать грибы! '

    bot.send_message(message.chat.id, f' {welcome_text} Oтправь мне гриб, который ты хочешь распознать!')

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    if not message.photo:
        return bot.send_message(message.chat.id, 'Вы забыли загрузить картинку ;/')
    file_info = bot.get_file(message.photo[-1].file.id)
    file_name = file_info.file_path.split('/')[-1]


    download_file = bot.download_file(file_info.file_path)
    image_path = f'images/{file_name}'
    with open(f'images/{file_name}','wb') as new_file:
        new_file.write(download_file)


    #обрабатываем фото и отправляем результаты
    mushroom_name, percentage = get_class(image_path)
    bot.send_message(message.chat.id, f'С вероятностью {percentage}% на фото {mushroom_name}')
bot.polling()