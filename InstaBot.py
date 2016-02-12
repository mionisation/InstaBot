import yaml, re, time, sys, hmac
import instagram
import logging
import schedule
import state
import sys
from datetime import date
from os import path
import random

INSTAGRAM_API = 'https://api.instagram.com/v1'
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'

def unicode_print(s):
    ''' Handles various troubles with unicode console output. '''
    logging.debug(s.encode(sys.stdout.encoding or 'ascii', 'backslashreplace'))

def like_hashtags(schedule, client, state):
    ''' Function to like hashtages. '''
    logging.info('Started to like by hashtags')
    while True:
        media_id = schedule.next()
        try:
            client.like(media_id)
        except instagram.APIError as e:
#            status_code = int(e.status_code)
#            if status_code in (403, 429):
#                logging.debug(' TOO MANY REQUESTS')
#                logging.debug(e)
#                return
            logging.debug('SOMETHING WENT WRONG')
            logging.debug(e)
            logging.debug('SLEEPING FOR 60 seconds')
            time.sleep(60)
        else:
            logging.debug(' YOU LIKED %s' % media_id)
            state.increment(str(date.today()))
            waitingtime = random.uniform(configuration['SLEEPTIME_UPPERBOUND'], configuration['SLEEPTIME_LOWERBOUND'])
            time.sleep(waitingtime)

if __name__ == '__main__':
    directory = path.abspath(path.dirname(__file__))
    configuration_filename = path.join(directory, 'configuration.yml')
    configuration = yaml.safe_load(open(configuration_filename, "r"))
    logging.basicConfig(filename=path.join(directory, 'log.log'), level=logging.DEBUG)

    client = instagram.Client()
    client.login(configuration['CREDENTIALS']['LOGIN'], configuration['CREDENTIALS']['PASSWORD'])

    current_state = state.State(path.join(directory, 'state.yml'))
    _schedule = schedule.Schedule(
        hashtags_filename=path.join(directory, 'hashtags.txt'),
        configuration=configuration,
        state=current_state,
    )
    like_hashtags(
        schedule=_schedule,
        client=client,
        state=current_state,
    )
