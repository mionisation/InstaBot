import re
import requests
import urllib

WEBSTA_URL = 'http://websta.me/'

class ScheduleError(Exception):
    pass

class Schedule(object):
    def __init__(self, hashtags_filename, configuration, state):
        self._configuration = configuration
        self._hashtags = self._get_hashtags_from_file(hashtags_filename)
        self._state = state
        self._update_media_ids(self._get_current_hashtag())

    def next(self):
        media_id_index = self._state.increment('schedule_media_id_index', 0)
        if media_id_index >= len(self._media_ids) or media_id_index >= self._configuration['PERHASHTAG']:
            media_id_index = 0
            self._state['schedule_media_id_index'] = media_id_index
            self._update_media_ids(self._get_next_hashtag())
        return self._media_ids[media_id_index]

    def _get_hashtags_from_file(self, filename):
        ''' Function to read the hashtags from a users file if not wanting to parse the top 100. '''
        hashtags = []
        f = open(filename, 'rb')
        # Strip newline character.
        hashtags = [unicode(line, 'utf-8').strip() for line in open(filename)]
        f.close()
        return hashtags

    def _get_current_hashtag(self):
        hashtag_index = self._state.get('schedule_hashtag_index', 0)
        try:
            hashtag = self._hashtags[hashtag_index]
        except IndexError:
            hashtag_index = 0
            try:
                hashtag = self._hashtags[hashtag_index]
            except IndexError:
                raise ScheduleError('Hashtags array is empty.')
            self._state['schedule_hashtag_index'] = hashtag_index
        return hashtag

    def _get_next_hashtag(self):
        hashtag_index = self._state.increment('schedule_hashtag_index', 0)
        try:
            hashtag = self._hashtags[hashtag_index]
        except IndexError:
            hashtag_index = 0
            try:
                hashtag = self._hashtags[hashtag_index]
            except IndexError:
                raise ScheduleError('Hashtags array is empty.')
            self._state['schedule_hashtag_index'] = hashtag_index
        return hashtag

    def _update_media_ids(self, hashtag):
        hashtag_url = WEBSTA_URL +'tag/' + urllib.quote(hashtag.encode('utf-8'))
        response = requests.get(hashtag_url)
        self._media_ids = re.findall('span class=\"like_count_(.*)\"', response.text)
