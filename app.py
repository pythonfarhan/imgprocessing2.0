import twitter
import  _constant
import requests
import tweepy
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import textwrap
import time

# python-twitter auth
def python_twitter():
    api = twitter.Api(consumer_key=_constant.consumer_key,
                      consumer_secret=_constant.consumer_secret,
                      access_token_key=_constant.access_token,
                      access_token_secret=_constant.access_token_secret,
                      sleep_on_rate_limit=True)
    return api

# tweepy auth
def twitterAuth():

    auth = tweepy.OAuthHandler(consumer_key=_constant.consumer_key, consumer_secret=_constant.consumer_secret)
    auth.set_access_token(key=_constant.access_token, secret=_constant.access_token_secret)
    api = tweepy.API(auth)

    return api

# download image function
def download(filename):
    url = 'https://picsum.photos/480/800/?random'
    r = requests.get(url=url)
    with open(filename, 'wb') as f:
        f.write(r.content)

# send tweet with media function
def tweetit(filename, text=None):
    api = twitterAuth()
    while True:
        try:
            api.update_with_media(filename=filename, status=text)
            print('%s was tweeted' % filename)
            break
        except Exception:
            pass

# notify sender
def postdm(username, message):
    api = python_twitter()
    while True:
        try:
            api.PostDirectMessage(screen_name=username, text=message)
            print("%s's dm was sent" % username)
            break
        except Exception:
            pass

# get latest tweet id for dm
def getTweetId():
    api = python_twitter()
    statuses = api.GetUserTimeline(screen_name='imgprocessing')
    return [i.id for i in statuses][0]

# get dm
def getDm():
    api = python_twitter()
    dm = api.GetDirectMessages(full_text=True, return_json=True)
    result = list()
    for i in range(len(dm)):
        text = dm[i]['text']
        id = dm[i]['id']
        sender = dm[i]['sender']['screen_name']
        d = dict(text=text, sender=sender, id=id)
        result.append(d)
        result.reverse()
    return result

def run():
    api = python_twitter()

    print("imgprocessing2.0 is running..")

    cache = str()

    dm = []

    while True:

        if len(dm) is not 0:

            for i in range(len(dm)):

                if dm[i]['text'].lower() == 'test':
                    dm.remove(dm[i])
                    continue

                if 'https://' in dm[i]['text']:
                    dm.remove(dm[i])
                    continue

                if dm[i]['text'].lower() == '#hehe':
                    dm.remove(dm[i])
                    continue

                if len(dm[i]['text']) <= 4:
                    dm.remove(dm[i])
                    continue

                if dm[i]['sender'] == cache:
                    # delete the message
                    message_id = dm[i]['id']
                    api.DestroyDirectMessage(message_id=message_id)
                    continue

                if len(dm[i]['text']) <= 1000:

                    if '#hehe' in dm[i]['text']:
                        # get and set sender screen_name
                        sender = dm[i]['sender']
                        caption = 'sender: %s (use #hehe if you want to show your screen name)' % sender

                        # get twitter dm text
                        message = dm[i]['text']

                        text = str(message).replace('#hehe', '')
                        text = textwrap.fill(text, width=40)

                        # download image
                        download('download.png')

                        # edit download.png and save it as background.png
                        downloadpng = Image.open('download.png')
                        enhancer = ImageEnhance.Brightness(downloadpng)
                        enhancer.enhance(0.5).save('background.png')

                        # write dm text on background.png
                        image = Image.open('background.png')
                        draw = ImageDraw.Draw(image)
                        (x, y) = (40, 70)
                        color = 'rgb(255, 255, 255)'
                        font = ImageFont.truetype('Roboto-Light.ttf', size=23)
                        draw.text((x, y), text=text, fill=color, font=font)

                        font = ImageFont.truetype('Roboto-Light.ttf', size=17)
                        footertext = 'twitter.com/imgprocessing - %s' % sender
                        draw.text((10, 760), text=footertext, font=font)

                        image.save('tweet.png')

                        # tweet the tweet.png
                        tweetit('tweet.png', text=caption)

                        # delete the message
                        message_id = dm[i]['id']
                        api.DestroyDirectMessage(message_id=message_id)

                        # notify sender
                        tweet_id = getTweetId()
                        url = 'https://twitter.com/%s/status/%s' % (sender, tweet_id)
                        notify = 'your dm was tweeted! %s' % url
                        postdm(username=sender, message=notify)

                        cache = sender

                        dm.remove(dm[i])

                        # make interval
                        time.sleep(60)

                    else:

                        # get sender name
                        sender = dm[i]['sender']

                        # get twitter dm text
                        message = dm[i]['text']
                        text = textwrap.fill(message, width=40)

                        # download image
                        download('download.png')

                        # edit download.png and save it as background.png
                        downloadpng = Image.open('download.png')
                        enhancer = ImageEnhance.Brightness(downloadpng)
                        enhancer.enhance(0.5).save('background.png')

                        # write dm text on background.png
                        image = Image.open('background.png')
                        draw = ImageDraw.Draw(image)
                        (x, y) = (40, 70)
                        color = 'rgb(255, 255, 255)'
                        font = ImageFont.truetype('Roboto-Light.ttf', size=22)
                        draw.text((x, y), text=text, fill=color, font=font)

                        font = ImageFont.truetype('Roboto-Light.ttf', size=15)
                        draw.text((10, 760), text='twitter.com/imgprocessing', font=font)

                        image.save('tweet.png')

                        # tweet the tweet.png
                        tweetit('tweet.png')

                        # delete the message
                        message_id = dm[i]['id']
                        api.DestroyDirectMessage(message_id=message_id)

                        # notify sender
                        tweet_id = getTweetId()
                        url = 'https://twitter.com/%s/status/%s' % (sender, tweet_id)
                        notify = 'your dm was tweeted! %s' % url
                        postdm(username=sender, message=notify)

                        cache = sender

                        dm.remove(dm[i])

                        # make interval
                        time.sleep(60)


        if len(dm) is 0:
            dm = getDm()
            print('dm reloaded')
            if len(dm) == 0:
                print('no dm, please wait..')
                time.sleep(60)




if __name__ == '__main__':
    run()

