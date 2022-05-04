import telebot
import config
from telebot import types
from cista import encode, decode
from io import BytesIO

bot = telebot.TeleBot(config.token)
sad = True
en_ = False
de_ = False
res = 0
images = dict()
wolk = 1
ric = 1


# start
@bot.message_handler(commands=['start'])
def start(massage):
#  тимо
    sti = open('file/bot_timo.webp', 'rb')
    bot.send_sticker(massage.chat.id, sti)
#  клава
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Начать 🏁')
    item2 = types.KeyboardButton('Функции бота 💻')
    markup.add(item1, item2)
#  приветствие
    bot.send_message(massage.chat.id, "Добро пожаловать, {0.first_name} ! 👋"
                                      "\nЯ бот шифровщик по имени Понки 🐰"
                                      "\nПриятно познакомиться! ❤".format(massage.from_user, bot.get_me()),
                                       reply_markup=markup, parse_mode='html')


# help
@bot.message_handler(commands=['help'])
def help(massage):
# выбор действий 🦾
    bot.send_message(massage.chat.id, "Выберите что вы хотите делать: Шифруем или Дешифруем"
                                      "\n /encode - Шифруем 🛬"
                                      "\n /decode - Дешифруем 🛫".format(massage.from_user, bot.get_me()))


# encode
@bot.message_handler(commands=['encode'])
def enc(massage):
    bot.send_message(massage.chat.id, "Инструкция по пользованию Шифровки: 🛬"
                                      "\n 1 - Ведите текст который вы хотите зашифровать"
                                      "\n 2 - Введите ключ, только благодоря ему ты сможешь разшифровать послание"
                                      "\n 3 - Выведите изображение в котором вы хотите спрятать послание".format(massage.from_user, bot.get_me()))


# decode
@bot.message_handler(commands=['decode'])
def dec(massage):
    bot.send_message(massage.chat.id, "Инструкция по пользованию Дешифровки: 🛫"
                                      "\n 1 - Введите ключ, помните что без ключа вы не сможене разшифровать послание"
                                      "\n 2 - Выведите изображение в котором спрятанно послание"
                                      " изображение должно быть такое каким вы его получили (не сжатым)".format(massage.from_user, bot.get_me()))


# информация о рользовании бота
@bot.message_handler(commands=['info'])
def info(massage):
    bot.send_message(massage.chat.id, "Сводка информации о Понки:"
                                      "\n 1 - это бот шифровщик, который шифрует ваше послание и изображении"
                                      "\n 2 - пока думаю".format(massage.from_user, bot.get_me()))


# начало шифровки
@bot.message_handler(commands=['en'])
def en(massage):
    global sad
    global en_
    sad = False
    en_ = True
    bot.send_message(massage.chat.id, 'Введите своё послание:')


# начало дешифровки
@bot.message_handler(commands=['de'])
def de(massage):
    global sad
    global de_
    sad = False
    de_ = True
    bot.send_message(massage.chat.id, 'Введите ключ:')


@bot.message_handler(commands=['stop'])
def chek(massage):
    global de_
    global en_
    global ric
    global wolk
    global sad
    global res
    ric = 1
    wolk = 1
    sad = True
    en_ = False
    de_ = False
    if res == 1:
        res = 0
    else:
       bot.send_message(massage.chat.id, 'если не понял нажми => /help')


# соновной блок действий
@bot.message_handler(content_types=['text'])
def calabs(massage):
    global sad
    global en_
    global de_
    global text_to_encrypt
    global private_key
    if sad:
        if massage.chat.type == 'private':
            if massage.text == 'Начать 🏁':
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                item1 = types.KeyboardButton('/en - Шифруем 🛬')
                item2 = types.KeyboardButton('/de - Дешифруем 🛫')
                markup.add(item1, item2)
                sti = open('file/fi.webp', 'rb')
                bot.send_sticker(massage.chat.id, sti)
                bot.send_message(massage.chat.id, 'Какие будут дальнейшие действия ?'
                                                  '\nих можно посмотреть здесь => /help', reply_markup=markup)

            elif massage.text == 'Функции бота 💻':
                bot.send_message(massage.chat.id, '  /info - информация о боте'
                                                  '\n/start - начало работы с ботом '
                                                  '\n/help - инструкция по пользованию ')
            else:
                bot.send_message(massage.chat.id, 'Ты по моему что-то перепутал 👾'
                                                  '\nесли не понял нажми => /help')
    if en_:
        global wolk
        if massage.chat.type == 'private':
            if wolk == 1:
                text_to_encrypt = massage.text
                bot.send_message(massage.chat.id, 'Придумайте ключ:')
            elif wolk == 2:
                private_key = massage.text
                bot.send_message(massage.chat.id, 'Вставьте изображение:')
            elif wolk == 3:
                bot.send_message(massage.chat.id, 'Это не изображение!'
                                                  '\nПортобуйте ещё раз:'
                                                  '\nЕсли хотите прервать шифровку напишите => /stop ')
                wolk -= 1

            wolk += 1
    if de_:
        global ric
        if massage.chat.type == 'private':
            if ric == 1:
                private_key = massage.text
                bot.send_message(massage.chat.id, 'Встальте изображение:')
            elif ric == 2:
                bot.send_message(massage.chat.id, 'Это не изображение!'
                                                  '\nПортобуйте ещё раз:'
                                                  '\nЕсли хотите прервать дешифровку напишите /stop ')
                ric -= 1
        ric += 1


@bot.message_handler(content_types=['photo'])
def code(massage):
    global res
    if wolk == 3:
        sti = open('file/ok.webp', 'rb')
        bot.send_sticker(massage.chat.id, sti)
        bot.reply_to(massage, f'Сообщение : - {text_to_encrypt} - успешно зашифрованно ')
        file_info = bot.get_file(massage.photo[len(massage.photo) - 1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        src = 'copy/' + file_info.file_path
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
        with open(src, 'rb') as file:
            img_data = file.read()
        crypto_img = encode(text_to_encrypt, private_key, BytesIO(img_data))
        file_path = file_info.file_path
        file_name = '.'.join(file_path.split('/')[-1].split('.')[:-1]) + '.png'
        crypto_img.save(f'copy/crypto-{file_name}')
        name = file_name.split('/')[-1]
        bot.send_document(massage.chat.id, open(f'copy/crypto-{name}', 'rb'))
        res += 1
        bot.reply_to(massage, 'Для продолжения => /stop')
    else:
        sti = open('file/sory.webp', 'rb')
        bot.send_sticker(massage.chat.id, sti)
        bot.reply_to(massage, 'Выделаете что-то не так'
                              '\n если что жми => /stop')


@bot.message_handler(content_types=['document'])
def code_(massage):
    global res
    if ric == 2:
        sticker_id = massage.document.file_id
        file_info = bot.get_file(sticker_id)
        downloaded_file = bot.download_file(file_info.file_path)
        src = 'photo/' + file_info.file_path
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
        with open(src, 'rb') as file:
            img_data = file.read()
        sti = open('file/end.webp', 'rb')
        bot.send_sticker(massage.chat.id, sti)
        bot.reply_to(massage, f'Сообщение : - {decode(private_key, BytesIO(img_data))}'
                              f' - было спрятанно в этом изображении')

        res += 1
        bot.reply_to(massage, 'Для продолжения => /stop')

    else:
        sti = open('file/sory.webp', 'rb')
        bot.send_sticker(massage.chat.id, sti)
        bot.reply_to(massage, 'Выделаете что-то не так'
                              '\n если что жми => /stop')


if __name__ == '__main__': # чтобы код выполнялся только при запуске в виде сценария, а не при импорте модуля
    try:
       bot.polling(none_stop=True) # запуск бота
    except Exception as e:
       print(e) # или import traceback; traceback.print_exc() для печати полной инфы
