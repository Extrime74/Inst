from telebot import types
import function
import telebot
import config


bot = telebot.TeleBot(config.TOKEN)
fu = function

fu.inst_login()


@bot.message_handler(commands=['start'])
def start(start_message):

    if start_message.chat.id == config.MY_USER_ID:
        bot.send_message(start_message.from_user.id,
                         f'👋 Привет, {start_message.from_user.first_name}!'
                         f'\nПоделись со мной фото или видео и я загружу их в твой инстаграм!')

        @bot.message_handler(content_types=['photo'])
        def photo(photo_message):

            photo_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            photo_btn1 = types.KeyboardButton('Выложить фото в ленту')
            photo_btn2 = types.KeyboardButton('Выложить фото в сторис')
            photo_markup.add(photo_btn1, photo_btn2)
            bot.send_message(photo_message.from_user.id, 'Куда выложить фото❓', reply_markup=photo_markup)

            fu.photo_cleanup()
            fileid = photo_message.photo[-1].file_id
            file_info = bot.get_file(fileid)
            downloaded_file = bot.download_file(file_info.file_path)
            with open("image.jpg", 'wb') as new_file:
                new_file.write(downloaded_file)

            @bot.message_handler(content_types=['text'])
            def photo_to_feed(photo_to_message):

                if photo_to_message.text == 'Выложить фото в ленту':
                    bot.send_photo('-1001660390862', fileid)
                    status = fu.photo_upload_feed()
                    if status == 'OK':
                        bot.reply_to(photo_to_message, 'Запостил.')
                    else:
                        bot.reply_to(photo_to_message, 'Что-то пошло не так.')

                if photo_to_message.text == 'Выложить фото в сторис':
                    bot.send_photo('-1001660390862', fileid)
                    status = fu.photo_upload_story()
                    if status == 'OK':
                        bot.reply_to(photo_to_message, 'Запостил.')
                    else:
                        bot.reply_to(photo_to_message, 'Что-то пошло не так.')

        @bot.message_handler(content_types=['video'])
        def video(video_message):

            video_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            video_btn1 = types.KeyboardButton('Выложить видео в ленту')
            video_btn2 = types.KeyboardButton('Выложить видео в сторис')
            video_markup.add(video_btn1, video_btn2)
            bot.send_message(video_message.from_user.id, 'Куда выложить видео❓', reply_markup=video_markup)

            @bot.message_handler(content_types=['text'])
            def video_to_feed(video_to_message):

                if video_to_message.text == 'Выложить видео в ленту':
                    fu.video_cleanup()
                    fileid = video_message.video.file_id
                    file_info = bot.get_file(fileid)
                    downloaded_file = bot.download_file(file_info.file_path)
                    with open('video.mp4', 'wb') as new_file:
                        new_file.write(downloaded_file)
                    bot.send_video('-1001660390862', fileid)
                    status = fu.video_upload_feed()
                    if status == 'OK':
                        bot.reply_to(video_to_message, 'Запостил.')
                    else:
                        bot.reply_to(video_to_message, 'Что-то пошло не так.\nВозможно, видео слишком длинное.')

                if video_to_message.text == 'Выложить видео в сторис':
                    fu.video_cleanup()
                    fileid = video_message.video.file_id
                    file_info = bot.get_file(fileid)
                    downloaded_file = bot.download_file(file_info.file_path)
                    with open('video.mp4', 'wb') as new_file:
                        new_file.write(downloaded_file)
                    bot.send_video('-1001660390862', fileid)
                    status = fu.video_upload_story()
                    if status == 'OK':
                        bot.reply_to(video_to_message, 'Запостил.')
                    else:
                        bot.reply_to(video_to_message, 'Что-то пошло не так.\nВозможно, видео слишком длинное.')

    else:
        bot.reply_to(start_message, 'Сорян, этот бот приватный!')


bot.polling(none_stop=True, interval=0)


# @bot.message_handler(content_types=['text'])
# def get_text_messages(message):
#     if message.text == 'Поздороваться 👋 ':
#         markup = types.ReplyKeyboardMarkup(resize_keyboard=True)  # создание новых кнопок
#         btn1 = types.KeyboardButton('Выложить фото в ленту')
#         btn2 = types.KeyboardButton('Выложить фото в сторис')
#         btn3 = types.KeyboardButton('Выложить видео в ленту')
#         btn4 = types.KeyboardButton('Выложить видео в сторис')
#         btn5 = types.KeyboardButton('Выложить видео в Reels')
#         markup.add(btn1, btn2, btn3, btn4, btn5)
#         bot.send_message(message.from_user.id, 'Что ты хочешь сделать❓', reply_markup=markup)

# @bot.message_handler(content_types=['photo'])
# def photo(message):
#     fu.photo_cleanup()
#     bot.send_message(message.chat.id, 'Ты отправил мне фото')
#     fileid = message.photo[-1].file_id
#     file_info = bot.get_file(fileid)
#     downloaded_file = bot.download_file(file_info.file_path)
#     with open('image.jpg', 'wb') as new_file:
#         new_file.write(downloaded_file)
#     bot.send_photo('-1001660390862', fileid)
#     fu.photo_upload()
#     bot.reply_to(message, "Запостил")
