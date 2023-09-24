from instagrapi import Client
from instagrapi.exceptions import LoginRequired
import config
import logging


cl = Client()
logger = logging.getLogger()


# def runproxy():
#     before_ip = cl._send_public_request("https://api.ipify.org/")
#     cl.set_proxy("socks5://wRQUNy:Zzka72@168.181.55.181:8000")
#     after_ip = cl._send_public_request("https://api.ipify.org/")
#     print(f"Before: {before_ip}")
#     print(f"After: {after_ip}")

def login_user():                                   # Логин в инстаграм, используя сессию.
    session = cl.load_settings("session.json")
    login_via_session = False
    login_via_pw = False

    if session:
        try:
            cl.set_settings(session)
            cl.login(config.USERNAME, config.PASSWORD)

            # check if session is valid
            try:
                cl.get_timeline_feed()
            except LoginRequired:
                logger.info("Session is invalid, need to login via username and password")
                old_session = cl.get_settings()

                # use the same device uuids across logins
                cl.set_settings({})
                cl.set_uuids(old_session["uuids"])
                cl.login(config.USERNAME, config.PASSWORD)
            login_via_session = True
        except Exception as e:
            logger.info("Couldn't login user using session information: %s" % e)

    if not login_via_session:
        try:
            logger.info("Attempting to login via username and password. username: %s" % config.USERNAME)
            if cl.login(config.USERNAME, config.PASSWORD):
                login_via_pw = True
        except Exception as e:
            logger.info("Couldn't login user using username and password: %s" % e)

    if not login_via_pw and not login_via_session:
        raise Exception("Couldn't login user with either password or session")

def inst_login():                                # Функция логина в инстаграм.
    login_user()                                 # Логинимся при запуске бота.
    cl.get_timeline_feed()                       # Обновляем ленту, чтобы замаскироваться под реального человека.
    name = cl.account_info().full_name           # Достаем имя акканта в инстаграм.
    print(f'Добро пожаловать в аккаунт {name}')
