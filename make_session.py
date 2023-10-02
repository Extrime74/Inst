from instagrapi import Client
import config

# cl = Client(proxy=config.PROXY)
cl = Client()
cl.login(config.USERNAME, config.PASSWORD)
cl.delay_range = [1, 3]
cl.dump_settings('session.json')
print('Done')
