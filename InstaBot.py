import yaml, re, time, sys, hmac, requests, urllib
import instagram
import sys
from hashlib import sha256
from os import path

WEBSTA_URL = 'http://websta.me/'
WEBSTA_HASHTAG = WEBSTA_URL + 'hot'

INSTAGRAM_API = 'https://api.instagram.com/v1'
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'

def unicode_print(s):
    ''' Handles various troubles with unicode console output. '''
    print s.encode(sys.stdout.encoding or 'ascii', 'backslashreplace')

def get_top_hashtags():
    ''' Function to parse the Top HashTag page and get the current top hashtags. '''
    response = requests.get(WEBSTA_HASHTAG)
    topHashtags = re.findall('\"\>#(.*)\<\/a\>\<\/strong\>', response.text)
    return topHashtags

def get_hashtags_from_file(filename):
    ''' Function to read the hashtags from a users file if not wanting to parse the top 100. '''
    #your list of hashtags
    hashtags = []
    #Hashtag file input
    f = open(filename)
    #strips newline character
    hashtags = [unicode(line.strip(), 'utf-8') for line in open(filename)]
    f.close()
    return hashtags

def like_hashtags(hashtags, client):
    ''' Function to like hashtages. '''
    likes = 0

    for hashtag in hashtags:
        hashtaglikes = 0
        media_id = []
        hashtag_url = WEBSTA_URL +'tag/' + urllib.quote(hashtag.encode('utf-8'))
        response = requests.get(hashtag_url)
        unicode_print(u'Liking #%s' % hashtag)
        media_ids = re.findall('span class=\"like_count_(.*)\"', response.text)

        for media_id in media_ids:
            if profile['MAXLIKES'] == 'NO_MAX':
                pass
            elif likes >= int(profile['MAXLIKES']):
                print 'You have reached MAX_LIKES(%d)' % profile['MAXLIKES']
                unicode_print(u'This # is currently %s' % hashtag)
                sys.exit()
                break

            if profile['PERHASHTAG'] == "NO_MAX":
                pass
            elif hashtaglikes >= int(profile['PERHASHTAG']):
                print 'REACHED MAX_LIKES PER HASHTAG'
                print 'MOVING ONTO NEXT HASHTAG'
                hashtaglikes = 0
                break

            try:
                client.like(media_id)
            except instagram.APIError as e:
                status_code = int(e.status_code)
                if status_code in (403, 429):
                    print ' TOO MANY REQUESTS'
                    print e
                    return
                print 'SOMETHING WENT WRONG'
                print e
                print 'SLEEPING FOR 60 seconds'
                print 'CURRENTLY LIKED %d photos' % likes
                time.sleep(60)
            else:
                print ' YOU LIKED %s' % media_id
                likes += 1
                hashtaglikes += 1
                time.sleep(profile['SLEEPTIME'])

    print 'YOU LIKED %d photos' % likes

if __name__ == '__main__':
    print '================================='
    print '            InstaBot             '
    print '    Developed by Marc Laventure  '
    print '================================='
    print

    directory = path.abspath(path.dirname(__file__))
    profile_filename = path.join(directory, 'profile.yml')
    profile = yaml.safe_load(open(profile_filename, "r"))

    client = instagram.Client()
    client.login(profile['CREDENTIALS']['LOGIN'], profile['CREDENTIALS']['PASSWORD'])

    if profile['TOP'] == 1:
        hashtags = get_top_hashtags()
    else:
        hashtags_filename = path.join(directory, 'hashtags.txt')
        hashtags = get_hashtags_from_file(hashtags_filename)
    like_hashtags(hashtags, client)
