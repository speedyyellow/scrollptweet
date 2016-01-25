#import
import scrollphat
import sys
import time
import thread
from twython import TwythonStreamer

# Twitter auth keys here
APP_KEY = ''
APP_SECRET = ''
OAUTH_TOKEN = ''
OAUTH_TOKEN_SECRET = ''

#print
class MyStreamer(TwythonStreamer):
    def on_success(self, data):
        if 'text' in data:
            raw_tweet = '     @{}: {}'.format(data['user']['screen_name'].encode('utf-8'), data['text'].encode('utf-8'))
            tweet = self.remove_link(raw_tweet)
            scrollphat.write_string(tweet.upper())
            status_length = scrollphat.buffer_len()
            while status_length > 0:
                scrollphat.scroll()
                time.sleep(0.1)
                status_length -= 1

    def on_error(self, status_code, data):
        print status_code, data

    def remove_link(self, input_string):
        # find the first http in the string
        result = ""
        http_start = input_string.find("http")
        if http_start != -1:
            # look for a space after the start of the link
            http_end = input_string.find(" ", http_start)
            if http_end != -1:
                # we have the position of our link, extract it
                link = input_string[http_start:http_end+1]
                #and remove it from the input
                result = input_string.replace(link,"")
            else:
                # the link is the last think in the string so just truncate
                result = input_string[0:http_start]

            # we've removed the first link, recurse to see if there are any others
            return self.remove_link(result).strip(" ")

        else:
            return input_string


try:
    #init
    scrollphat.clear()
    scrollphat.rotate = True
    scrollphat.set_brightness(2)

    stream = MyStreamer(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    stream.user()

except KeyboardInterrupt:
    scrollphat.clear()
    sys.exit(-1)