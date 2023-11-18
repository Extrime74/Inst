from instagrapi import Client
import config
import datetime


current_date = datetime.datetime.now()
date = current_date.strftime('%d.%m.%y %H:%M')
cl = Client()

cl.login(config.USERNAME, config.PASSWORD)
cl.dump_settings("session.json")


print("####",date,"####", f"\nФайл сессии сохранен")
