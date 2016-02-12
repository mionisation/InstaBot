import logging
import mechanize
import urllib

BASE_URL = 'https://www.instagram.com/'

class APIError(Exception):
    def __init__(self, message, error):
        self.message = message + ' ' + str(error)
        try:
            self.status_code = error.getcode()
        except AttributeError as e:
            print "Attribute error occured"

class Client(object):
    def __init__(self):
        self._cookiejar = mechanize.CookieJar()
        self._browser = mechanize.Browser()
        self._browser.set_cookiejar(self._cookiejar)

    def _ajax(self, url, data=None, referer=BASE_URL):
        if isinstance(data, dict):
            data = urllib.urlencode(data)
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Referer': referer,
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:43.0) Gecko/20100101 Firefox/43.0',
            'X-CSRFToken': self._csrf_token,
            'X-Instagram-AJAX': '1',
            'X-Requested-With': 'XMLHttpRequest',
        }
        request = mechanize.Request(
            BASE_URL + url,
            data=data,
            headers=headers,
        )
        self._cookiejar.add_cookie_header(request)
        try:
            response = self._browser.open(request)
        except Exception as e:
            e = APIError('Error during making AJAX request.', e)
            e.status_code = e.status_code
            raise e
        return response

    def _get_cookie(self, name):
        for cookie in self._cookiejar:
            if cookie.name == name:
                return cookie.value
        raise KeyError()

    def like(self, media_id):
        self._ajax('web/likes/%s/like/' % media_id, data='')

    def login(self, login, password):
        login_page_url = BASE_URL
        response = self._browser.open(login_page_url)
        self._update_csrf_token()
        login_response = self._ajax('accounts/login/ajax/', referer=login_page_url, data={
            'username': login,
            'password': password,
        })
        self._update_csrf_token() # CSRF token is refreshed after login request.

    def _update_csrf_token(self):
        self._csrf_token = self._get_cookie('csrftoken')
        logging.debug('csrftoken is %s', self._csrf_token)
