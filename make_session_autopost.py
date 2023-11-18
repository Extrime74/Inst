from instagrapi import Client
import config
import datetime


current_date = datetime.datetime.now()
date = current_date.strftime('%d.%m.%y %H:%M')
cl = Client(proxy=config.PROXY)

cl.login(config.USERNAME, config.PASSWORD)
cl.dump_settings("session_autopost.json")


print("####",date,"####", f"\nФайл сессии autopost сохранен")