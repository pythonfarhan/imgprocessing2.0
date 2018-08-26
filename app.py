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
    return result

def run():
    api = python_twitter()

    print("imgprocessing2.0 is running..")

    cache = str()
    list_of_sender = list()

    while True:

        dm = getDm()

        if dm is not None:

            for i in dm:

                if i['sender'] in list_of_sender: continue

                if i['text'].lower() == 'test': continue

                if len(i['text']) <= 4: continue

                if i['sender'] == cache:
                    # delete the message
                    message_id = i['id']
                    api.DestroyDirectMessage(message_id=message_id)
                    continue

                if len(i['text']) <= 1000:

                    if '#hehe' in i['text']:
                        # get and set sender screen_name
                        sender = i['sender']
                        caption = 'sender: %s (use #hehe if you want to show your screen name)' % sender

                        # get twitter dm text
                        message = i['text']

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
                        font = ImageFont.truetype('Roboto-Light.ttf', size=22)
                        draw.text((x, y), text=text, fill=color, font=font)

                        font = ImageFont.truetype('Roboto-Light.ttf', size=15)
                        draw.text((10, 760), text='twitter.com/imgprocessing', font=font)

                        image.save('tweet.png')

                        # tweet the tweet.png
                        tweetit('tweet.png', text=caption)

                        # delete the message
                        message_id = i['id']
                        api.DestroyDirectMessage(message_id=message_id)

                        # notify sender
                        tweet_id = getTweetId()
                        url = 'https://twitter.com/%s/status/%s' % (sender, tweet_id)
                        notify = 'your dm was tweeted! %s' % url
                        postdm(username=sender, message=notify)

                        cache = sender
                        list_of_sender.append(sender)

                        # make interval
                        time.sleep(60)

                    else:

                        # get sender name
                        sender = i['sender']

                        # get twitter dm text
                        message = i['text']
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
                        message_id = i['id']
                        api.DestroyDirectMessage(message_id=message_id)

                        # notify sender
                        tweet_id = getTweetId()
                        url = 'https://twitter.com/%s/status/%s' % (sender, tweet_id)
                        notify = 'your dm was tweeted! %s' % url
                        postdm(username=sender, message=notify)

                        cache = sender
                        if sender not in list_of_sender:
                            list_of_sender.append(sender)

                        # make interval
                        time.sleep(60)
        if len(list_of_sender) is 40:
            list_of_sender = []




if __name__ == '__main__':
    run()

