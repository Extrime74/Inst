from threading import Timer
from instagrapi.exceptions import LoginRequired
from instagrapi.exceptions import UnknownError
from instagrapi import Client
import logging
import config
import os


cl = Client()
logger = logging.getLogger()


def login_user():    # взято из официальной документации instagrapi
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
                print('Сессия активна')
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
        raise Exception("Couldn't login user with either password or session") ##

def photo_cleanup():
    try:
        os.remove('image.jpg')
    except FileNotFoundError:
        pass

def video_cleanup():
    try:
        os.remove('video.mp4')
    except FileNotFoundError:
        pass

def photo_upload_feed():
    try:
        cl.photo_upload('image.jpg', caption='')
        cl.get_timeline_feed()
        print('Фото загружено в ленту')
        return 'OK'
    except Exception as e:
        print(f'Что-то пошло не так, {e}')
        pass

def photo_upload_story():
    try:
        cl.photo_upload_to_story('image.jpg', caption='')
        cl.get_timeline_feed()
        print('Фото загружено в сторис')
        return 'OK'
    except Exception as e:
        print(f'Что-то пошло не так, {e}')
        pass

def video_upload_feed():
    try:
        cl.video_upload('video.mp4', caption='')
        cl.get_timeline_feed()
        print('Видео загружено в ленту')
        return 'OK'
    except Exception as e:
        print(f'Что-то пошло не так, {e}')
        pass

def video_upload_story():
    try:
        cl.video_upload_to_story('video.mp4', caption='')
        cl.get_timeline_feed()
        print('Видео загружено в сторис')
        return 'OK'
    except Exception as e:
        print(f'Что-то пошло не так, {e}')
        pass
