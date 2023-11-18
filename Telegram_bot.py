import telebot
from telebot import types
import config
from pathlib import Path
import logging
from instagrapi import Client
from instagrapi.exceptions import LoginRequired
import os
import datetime


Path(f'Download/Photo/').mkdir(parents=True, exist_ok=True)
Path(f'Download/Video/').mkdir(parents=True, exist_ok=True)
cl = Client()
logger = logging.getLogger()
current_date = datetime.datetime.now()
date = current_date.strftime('%d.%m.%y %H:%M')
r = types.ReplyKeyboardRemove()

class PostingBot:
    def __init__(self):
        self.downloaded_file = None
        self.fileid = None
        self.token = config.TOKEN
        self.bot = telebot.TeleBot(self.token)

        print('\n#### Запусти бота в Telegram ####')

        def login_telebot():
            session = cl.load_settings('session.json')
            login_via_session = False
            login_via_pw = False

            if session:
                try:
                    cl.set_settings(session)
                    cl.login(config.USERNAME, config.PASSWORD)

                    # check if session is valid
                    try:
                        cl.get_timeline_feed()
                        print("\n####", date, "####", "\nСессия активна\n")
                    except LoginRequired:
                        logger.info('Session is invalid, need to login via username and password')
                        print('Session is invalid, need to login via username and password')
                        old_session = cl.get_settings()

                        # use the same device uuids across logins
                        cl.set_settings({})
                        cl.set_uuids(old_session['uuids'])
                        cl.login(config.USERNAME, config.PASSWORD)
                    login_via_session = True
                except Exception as e:
                    logger.info("Couldn't login user using session information: %s" % e)
                    print("Couldn't login user using session information: %s" % e)

            if not login_via_session:
                try:
                    logger.info('Attempting to login via username and password. username: %s' % config.USERNAME)
                    print('Attempting to login via username and password. username: %s' % config.USERNAME)
                    if cl.login(config.USERNAME, config.PASSWORD):
                        login_via_pw = True
                except Exception as e:
                    logger.info("Couldn't login user using username and password: %s" % e)
                    print("Couldn't login user using username and password: %s" % e)

            if not login_via_pw and not login_via_session:
                print("Couldn't login user with either password or session")
                raise Exception("Couldn't login user with either password or session")

        @self.bot.message_handler(commands=['start'])
        def start_command(message):
            if message.chat.id == config.MY_USER_ID:
                login_telebot()
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
                    elif types_message.content_type == 'audio':
                        self.bot.send_message(types_message.chat.id, 'Ну и херню же ты слушаешь')
                    elif types_message.content_type == 'document':
                        self.bot.send_message(types_message.chat.id, 'Ты где это взял?')
                    elif types_message.content_type == 'text':
                        self.bot.send_message(types_message.chat.id, 'Ну ты ваще')
                    elif types_message.content_type == 'location':
                        self.bot.send_message(types_message.chat.id, 'Опять где-то шляешься!')
                    elif types_message.content_type == 'contact':
                        self.bot.send_message(types_message.chat.id, 'Кореш твой?')
                    elif types_message.content_type == 'sticker':
                        self.bot.send_sticker(types_message.chat.id, 'CAACAgIAAxkBAAEKcahlHGuJCzjjAtM'
                                                                     'EpdK5ayCoL6NAnQACJhoAApmoyEtA7xJ_hrc3ajAE')
                    elif types_message.content_type == 'video_note':
                        self.bot.send_sticker(types_message.chat.id, 'CAACAgIAAxkBAAEKcahlHGuJCzjjAtM'
                                                                     'EpdK5ayCoL6NAnQACJhoAApmoyEtA7xJ_hrc3ajAE')

                @self.bot.message_handler(content_types=['photo'])
                def photo(photo_message):
                    try:
                        os.remove('image.jpg')
                    except Exception as e:
                        print("####", date, "####", e)
                        pass

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
                        try:
                            cl.photo_upload('image.jpg', caption='')
                            cl.get_timeline_feed()
                            print("####", date, "####", "\nФото загружено в ленту\n")
                            self.bot.send_message(photo_text_message.from_user.id, 'Запостил', reply_markup=r)
                        except Exception as e:
                            cl.get_timeline_feed()
                            print("####", date, "####", e)
                            self.bot.send_message(photo_text_message.from_user.id, e, reply_markup=r)
                            pass

                    elif photo_text_message.text == 'Выложить фото в сторис':
                        try:
                            cl.photo_upload_to_story('image.jpg', caption='')
                            cl.get_timeline_feed()
                            print("####", date, "####", "\nФото загружено в сторис\n")
                            self.bot.send_message(photo_text_message.from_user.id, 'Запостил', reply_markup=r)
                        except Exception as e:
                            cl.get_timeline_feed()
                            print("####", date, "####", e)
                            self.bot.send_message(photo_text_message.from_user.id, e, reply_markup=r)
                            pass

                    elif photo_text_message.text == 'Сохранить в хранилище':
                        src = f'Download/Photo/' + str(photo_text_message.date) + '.jpg'
                        with open(src, 'wb') as new_file:
                            new_file.write(self.downloaded_file)
                        self.bot.send_message(photo_text_message.from_user.id, 'Сохранил', reply_markup=r)

                @self.bot.message_handler(content_types=['video'])
                def video(video_message):

                    try:
                        os.remove('video.mp4')
                    except Exception as e:
                        print("####", date, "####", e)
                        pass
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
                        try:
                            cl.video_upload('video.mp4', caption='')
                            cl.get_timeline_feed()
                            print("####", date, "####", "\nВидео загружено в ленту\n")
                            self.bot.send_message(video_text_message.from_user.id, 'Запостил', reply_markup=r)
                        except Exception as e:
                            cl.get_timeline_feed()
                            print("####", date, "####", e)
                            self.bot.send_message(video_text_message.from_user.id, e, reply_markup=r)
                            pass

                    elif video_text_message.text == 'Выложить видео в сторис':
                        try:
                            cl.video_upload_to_story('video.mp4', caption='')
                            cl.get_timeline_feed()
                            print("####", date, "####", "\nВидео загружено в сторис\n")
                            self.bot.send_message(video_text_message.from_user.id, 'Запостил', reply_markup=r)
                        except Exception as e:
                            cl.get_timeline_feed()
                            print("####", date, "####", e)
                            self.bot.send_message(video_text_message.from_user.id, e, reply_markup=r)
                            pass

                    elif video_text_message.text == 'Сохранить в хранилище':
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
