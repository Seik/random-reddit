import HTMLParser
import datetime
import logging
import random
import threading

import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# as an object that auto updates itself
class Redditor(object):
    def __init__(self, subreddit, update_time=120):
        '''
        :param subreddit: name of the subreddit
        :param update_time: time between updates
        '''
        self.subreddit = subreddit
        self.json_obj = ''
        self.update_time = update_time
        threading.Thread(target=self.update()).start()

    def update(self):
        try:
            self.json_obj = requests.get(
                'https://www.reddit.com/r/{}/new.json?limit=100'.format(self.subreddit),
                headers={'User-agent': 'python scrapper'}
            ).json()
            logger.info('Updated json - {}'.format(datetime.datetime.now()))
        except Exception as e:
            logger.error(e.message)
        threading.Timer(self.update_time, self.update).start()

    def get_random(self):
        '''
        :return: url
        '''
        post = random.choice(self.json_obj['data']['children'])
        url = HTMLParser.HTMLParser().unescape(post['data']['url'])

        return url


# as a function
def get_random(subreddit):
    '''
    :param subreddit: name of the subreddit
    :return: url
    '''
    try:
        json_obj = requests.get(
            'https://www.reddit.com/r/{}/random.json'.format(subreddit),
            headers={'User-agent': 'python scrapper'}
        ).json()

        post = json_obj[0]['data']['children'][0]
        url = HTMLParser.HTMLParser().unescape(post['data']['url'])

        return url
    except Exception as e:
        logger.error(e.message)
        return ''
