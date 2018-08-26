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
    print('dm reloaded')
    return result

# get message
def getMessage(text=str()):
    if '[' in text and ']' in text:
        text = text[text.find('[')+1:text.find(']')]
        return text
    return None

def run():

    api = python_twitter()

    print("imgprocessing2.0 is running..")

    # handle duplicate text by sender
    cache = str()

    list_of_text = list()

    dm = []

    lap = str()

    while True:

        if len(dm) is not 0:

            for i in range(len(dm)):

                textdm = getMessage(dm[i]['text'])

                if textdm is None:
                    print('index %s was ignored because not use []')
                    continue

                if textdm is not None:

                    if textdm in list_of_text:
                        print('index %s was ignored because in list_of_text' % i)
                        if lap is '' and str(i) not in lap:
                            lap = str(i)
                            continue
                        if i == lap:
                            dm = getDm()
                            print('please wait')
                            time.sleep(60)


                    if textdm.lower() == 'test':
                        print('index %s was ignored because using test' % i)
                        continue

                    if 'https://' in textdm:
                        print('index %s was ignored because posting link' % i)
                        continue

                    if textdm.lower() == '#hehe':
                        print('index %s was ignored because using only #hehe without any message' % i)
                        continue

                    if len(textdm) <= 4:
                        print('index %s was ignored length of message is less than 4' % i)
                        continue

                    if dm[i]['sender'] == cache:
                        # delete the message
                        message_id = dm[i]['id']
                        api.DestroyDirectMessage(message_id=message_id)
                        print('index %s was ignored because in cache' % i)
                        continue

                    if len(textdm) <= 1000:

                        if '#hehe' in textdm:
                            # get and set sender screen_name
                            sender = dm[i]['sender']
                            caption = 'sender: %s (use #hehe if you want to show your screen name)' % sender

                            # get twitter dm text
                            message = textdm

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
                            print('index of %s' % i)

                            # delete the message
                            message_id = dm[i]['id']
                            api.DestroyDirectMessage(message_id=message_id)

                            # notify sender
                            tweet_id = getTweetId()
                            url = 'https://twitter.com/%s/status/%s' % (sender, tweet_id)
                            notify = 'your dm was tweeted! %s' % url
                            postdm(username=sender, message=notify)

                            cache = sender
                            if textdm not in list_of_text:
                                list_of_text.append(textdm)

                            # make interval
                            time.sleep(60)

                        else:

                            # get sender name
                            sender = dm[i]['sender']

                            # get twitter dm text
                            message = textdm
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
                            print('index of %s' % i)

                            # delete the message
                            message_id = dm[i]['id']
                            api.DestroyDirectMessage(message_id=message_id)

                            # notify sender
                            tweet_id = getTweetId()
                            url = 'https://twitter.com/%s/status/%s' % (sender, tweet_id)
                            notify = 'your dm was tweeted! %s' % url
                            postdm(username=sender, message=notify)

                            cache = sender
                            if textdm not in list_of_text:
                                list_of_text.append(textdm)

                            # make interval
                            time.sleep(60)



                if i == (len(dm) - 1):
                    dm = getDm()
                    if len(dm) == 0:
                        print('no dm, please wait..')
                        time.sleep(60)


        if len(list_of_text) is 40:
            list_of_text = []

        if len(dm) is 0:
            dm = getDm()
            if len(dm) == 0:
                print('no dm, please wait..')
                time.sleep(60)




if __name__ == '__main__':
    run()

