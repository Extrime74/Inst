import random
import time
from instagrapi import Client
import os
from instagrapi.exceptions import LoginRequired
import config
import telebot
import datetime
import logging

cl = Client()
logger = logging.getLogger()
current_date = datetime.datetime.now()
date = current_date.strftime('%d.%m.%y %H:%M')


def login_autopost():
    session = cl.load_settings('session_autopost.json')
    login_via_session = False
    login_via_pw = False

    if session:
        try:
            cl.set_settings(session)
            cl.login(config.USERNAME, config.PASSWORD)

            # check if session is valid
            try:
                cl.get_timeline_feed()
                print("####", date, "####", "\nСессия активна\n")
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


login_autopost()
print("####", date, "####", "\nАвтопостинг запущен\n")


class MakePost:
    def __init__(self, client):
        self.cl = client
        self.token = config.TOKEN
        self.bot = telebot.TeleBot(self.token)
        self.pic = ''

    def get_current_time(self):
        t = time.localtime()
        current_time = time.strftime('%H:%M:%S', t)
        return current_time

    def wait_for_time(self):
        while True:
            current_time = self.get_current_time()

            photo_feed_list = ['9:00:00', '17:00:00']
            photo_stories_list = ['13:00:00', '21:00:00']
            video_feed_list = ['11:00:00', '19:00:00']
            video_stories_list = ['15:00:00']

            if current_time in photo_feed_list:
                try:
                    pic = str("Download/Photo/") + (random.choice(os.listdir("Download/Photo/")))
                    time.sleep(2)
                    cl.photo_upload(caption='', path=pic)
                    print(current_time, 'Запостил фото в ленту', pic)
                    time.sleep(2)
                    self.bot.send_message('PUT_YOUR_TG_CHAT_ID_HERE', 'Запостил фото в ленту')
                    time.sleep(2)
                    os.remove(pic)
                except Exception as e:
                    print(current_time, e)
                    time.sleep(2)
                    self.bot.send_message('PUT_YOUR_TG_CHAT_ID_HERE', e)
                    pass

            elif current_time in photo_stories_list:
                try:
                    pic = str("Download/Photo/") + (random.choice(os.listdir("Download/Photo/")))
                    time.sleep(2)
                    cl.photo_upload_to_story(caption='', path=pic)
                    print(current_time, 'Запостил фото в сторис', pic)
                    time.sleep(2)
                    self.bot.send_message('PUT_YOUR_TG_CHAT_ID_HERE', 'Запостил фото в сторис')
                    time.sleep(2)
                    os.remove(pic)
                except Exception as e:
                    print(current_time, e)
                    time.sleep(2)
                    self.bot.send_message('PUT_YOUR_TG_CHAT_ID_HERE', e)
                    pass

            elif current_time in video_feed_list:
                try:
                    video = str("Download/Video/") + (random.choice(os.listdir("Download/Video/")))
                    time.sleep(2)
                    cl.video_upload(caption='', path=video)
                    print(current_time, 'Запостил видео в ленту', video)
                    time.sleep(2)
                    self.bot.send_message('PUT_YOUR_TG_CHAT_ID_HERE', 'Запостил видео в ленту')
                    time.sleep(2)
                    os.remove(video)
                    os.remove(video + '.jpg')
                except Exception as e:
                    print(current_time, e)
                    time.sleep(2)
                    self.bot.send_message('PUT_YOUR_TG_CHAT_ID_HERE', e)
                    pass

            elif current_time in video_stories_list:
                try:
                    video = str("Download/Video/") + (random.choice(os.listdir("Download/Video/")))
                    time.sleep(2)
                    cl.video_upload_to_story(caption='', path=video)
                    print(current_time, 'Запостил видео в сторис', video)
                    time.sleep(2)
                    self.bot.send_message('PUT_YOUR_TG_CHAT_ID_HERE', 'Запостил видео в сторис')
                    time.sleep(2)
                    os.remove(video)
                    os.remove(video + '.jpg')
                except Exception as e:
                    print(current_time, e)
                    time.sleep(2)
                    self.bot.send_message('PUT_YOUR_TG_CHAT_ID_HERE', e)
                    pass


start = MakePost(cl)
start.wait_for_time()
