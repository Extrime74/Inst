from instagrapi import Client
import config

cl = Client()
cl.login(config.USERNAME, config.PASSWORD)
cl.dump_settings("session.json")
