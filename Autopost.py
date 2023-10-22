import random
import time
import function
from instagrapi import Client
import os
import config
import telebot

cl = Client()
function.login_user()
print('Погнали!')

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
                    pic = str("Download/Photo/")+(random.choice(os.listdir("Download/Photo/")))
                    time.sleep(2)
                    cl.photo_upload(caption='', path=pic)
                    self.bot.send_message('PUT_YOUR_TG_ID_HERE', 'Запостил фото в ленту')
                    print(current_time, 'Запостил фото в ленту', pic)
                    os.remove(pic)
                except Exception as e:
                    print(current_time, e)
                    self.bot.send_message('PUT_YOUR_TG_ID_HERE', f'Что-то пошло не так. {e}')
                    pass

            elif current_time in photo_stories_list:
                try:
                    pic = str("Download/Photo/")+(random.choice(os.listdir("Download/Photo/")))
                    time.sleep(2)
                    cl.photo_upload_to_story(caption='', path=pic)
                    self.bot.send_message('PUT_YOUR_TG_ID_HERE', 'Запостил фото в сторис')
                    print(current_time, 'Запостил фото в сторис', pic)
                    os.remove(pic)
                except Exception as e:
                    print(current_time, e)
                    self.bot.send_message('PUT_YOUR_TG_ID_HERE', f'Что-то пошло не так. {e}')
                    pass

            elif current_time in video_feed_list:
                try:
                    video = str("Download/Video/")+(random.choice(os.listdir("Download/Video/")))
                    time.sleep(2)
                    cl.video_upload(caption='', path=video)
                    self.bot.send_message('PUT_YOUR_TG_ID_HERE', 'Запостил видео в ленту')
                    print(current_time, 'Запостил видео в ленту', video)
                    os.remove(video)
                    os.remove(video + '.jpg')
                except Exception as e:
                    print(current_time, e)
                    self.bot.send_message('PUT_YOUR_TG_ID_HERE', f'Что-то пошло не так. {e}')
                    pass

            elif current_time in video_stories_list:
                try:
                    video = str("Download/Video/") + (random.choice(os.listdir("Download/Video/")))
                    time.sleep(2)
                    cl.video_upload_to_story(caption='', path=video)
                    self.bot.send_message('PUT_YOUR_TG_ID_HERE', 'Запостил видео в сторис')
                    print(current_time, 'Запостил видео в сторис', video)
                    os.remove(video)
                    os.remove(video + '.jpg')
                except Exception as e:
                    print(current_time, e)
                    self.bot.send_message('PUT_YOUR_TG_ID_HERE', f'Что-то пошло не так. {e}')
                    pass


start = MakePost(cl)
start.wait_for_time()
