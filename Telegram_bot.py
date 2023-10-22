import random
import time
import telebot
from telebot import types
import config
import function
from pathlib import Path
from instagrapi import Client
import os


Path(f'Download/Photo/').mkdir(parents=True, exist_ok=True)
Path(f'Download/Video/').mkdir(parents=True, exist_ok=True)


class PostingBot:
    def __init__(self):
        self.downloaded_file = None
        self.fileid = None
        self.token = config.TOKEN
        self.bot = telebot.TeleBot(self.token)
        r = types.ReplyKeyboardRemove()

        print('Запусти бота в Telegram')

        @self.bot.message_handler(commands=['start'])
        def start_command(message):
            if message.chat.id == config.MY_USER_ID:
                function.login_user()
                self.bot.send_message(message.from_user.id, f'👋 Привет, {message.from_user.first_name}!'
                                                            f'\nПоделись со мной фото или видео и я загружу их '
                                                            f'в твой инстаграм!')

                @self.bot.message_handler(commands=['ping'])
                def send_welcome(ping_message):
                    self.bot.send_message(ping_message.from_user.id, 'Я тут')

                @self.bot.message_handler(content_types=['audio', 'voice', 'document', 'text', 'location', 'contact', 
                                                         'sticker', 'video_note'])
                def others(types_message):
                    if types_message.content_type == 'voice':
                        self.bot.send_message(types_message.chat.id, 'Ну все, ты огребаешь!')
                        self.bot.send_sticker(types_message.chat.id, 'CAACAgIAAxkBAAEKcaplHG8ULx1nbcG6DDvnJyIqxX'
                                                                     '-iFQAC5hMAAi8iyEvZrfyv1izExzAE')
                    if types_message.content_type == 'audio':
                        self.bot.send_message(types_message.chat.id, 'Ну и херню же ты слушаешь')
                    if types_message.content_type == 'document':
                        self.bot.send_message(types_message.chat.id, 'Ты где это взял?')
                    if types_message.content_type == 'text':
                        self.bot.send_message(types_message.chat.id, 'Ну ты ваще')
                    if types_message.content_type == 'location':
                        self.bot.send_message(types_message.chat.id, 'Опять где-то шляешься!')
                    if types_message.content_type == 'contact':
                        self.bot.send_message(types_message.chat.id, 'Кореш твой?')
                    if types_message.content_type == 'sticker':
                        self.bot.send_sticker(types_message.chat.id, 'CAACAgIAAxkBAAEKcahlHGuJCzjjAtM'
                                                                     'EpdK5ayCoL6NAnQACJhoAApmoyEtA7xJ_hrc3ajAE')
                    if types_message.content_type == 'video_note':
                        self.bot.send_sticker(types_message.chat.id, 'CAACAgIAAxkBAAEKcahlHGuJCzjjAtM'
                                                                     'EpdK5ayCoL6NAnQACJhoAApmoyEtA7xJ_hrc3ajAE')

                @self.bot.message_handler(content_types=['photo'])
                def photo(photo_message):

                    function.photo_cleanup()
                    self.fileid = photo_message.photo[-1].file_id
                    self.file_info = self.bot.get_file(self.fileid)
                    self.downloaded_file = self.bot.download_file(self.file_info.file_path)
                    with open("image.jpg", 'wb') as new_file:
                        new_file.write(self.downloaded_file)

                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    btn1 = types.KeyboardButton('Выложить фото в ленту')
                    btn2 = types.KeyboardButton('Выложить фото в сторис')
                    btn3 = types.KeyboardButton('Сохранить в хранилище')
                    markup.add(btn1, btn2, btn3)
                    self.bot.send_message(photo_message.from_user.id, 'Куда выложить фото❓', reply_markup=markup)
                    self.bot.register_next_step_handler(photo_message, photo_text)

                @self.bot.message_handler(content_types=['text'])
                def photo_text(photo_text_message):

                    if photo_text_message.text == 'Выложить фото в ленту':
                        status = function.photo_upload_feed()
                        if status == 'OK':
                            self.bot.send_message(photo_text_message.from_user.id, 'Запостил', reply_markup=r)
                        else:
                            self.bot.send_message(photo_text_message.from_user.id, 'Что-то пошло не так.',
                                                  reply_markup=r)

                    if photo_text_message.text == 'Выложить фото в сторис':
                        status = function.photo_upload_story()
                        if status == 'OK':
                            self.bot.send_message(photo_text_message.from_user.id, 'Запостил', reply_markup=r)
                        else:
                            self.bot.send_message(photo_text_message.from_user.id, 'Что-то пошло не так.',
                                                  reply_markup=r)

                    if photo_text_message.text == 'Сохранить в хранилище':
                        src = f'Download/Photo/' + str(photo_text_message.date) + '.jpg'
                        with open(src, 'wb') as new_file:
                            new_file.write(self.downloaded_file)
                        self.bot.send_message(photo_text_message.from_user.id, 'Сохранил', reply_markup=r)

                @self.bot.message_handler(content_types=['video'])
                def video(video_message):

                    function.video_cleanup()
                    self.fileid = video_message.video.file_id
                    self.file_info = self.bot.get_file(self.fileid)
                    self.downloaded_file = self.bot.download_file(self.file_info.file_path)
                    with open('video.mp4', 'wb') as new_file:
                        new_file.write(self.downloaded_file)

                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    btn1 = types.KeyboardButton('Выложить видео в ленту')
                    btn2 = types.KeyboardButton('Выложить видео в сторис')
                    btn3 = types.KeyboardButton('Сохранить в хранилище')
                    markup.add(btn1, btn2, btn3)
                    self.bot.send_message(video_message.from_user.id, 'Куда выложить видео❓', reply_markup=markup)
                    self.bot.register_next_step_handler(video_message, video_text)

                @self.bot.message_handler(content_types=['text'])
                def video_text(video_text_message):

                    if video_text_message.text == 'Выложить видео в ленту':
                        status = function.video_upload_feed()
                        if status == 'OK':
                            self.bot.send_message(video_text_message.from_user.id, 'Запостил.', reply_markup=r)
                        else:
                            self.bot.send_message(video_text_message.from_user.id,
                                                  'Что-то пошло не так.'
                                                  '\nВозможно, видео слишком длинное.',
                                                  reply_markup=r)

                    if video_text_message.text == 'Выложить видео в сторис':
                        status = function.video_upload_story()
                        if status == 'OK':
                            self.bot.send_message(video_text_message.from_user.id, 'Запостил.', reply_markup=r)
                        else:
                            self.bot.send_message(video_text_message.from_user.id,
                                                  'Что-то пошло не так.'
                                                  '\nВозможно, видео слишком длинное.',
                                                  reply_markup=r)

                    if video_text_message.text == 'Сохранить в хранилище':
                        src = f'Download/Video/' + str(video_text_message.date) + '.mp4'
                        with open(src, 'wb') as new_file:
                            new_file.write(self.downloaded_file)
                        self.bot.send_message(video_text_message.from_user.id, 'Сохранил', reply_markup=r)

            else:
                self.bot.reply_to(message, 'Сорян, этот бот приватный!')

    def run(self):
        self.bot.polling()


if __name__ == '__main__':
    Tele = PostingBot()
    Tele.run()
