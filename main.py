from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import textwrap
import time
import json
import _constant
import twitter
# original = Image.open('download.png')
# enhancer = ImageEnhance.Brightness(original)
#
# factor = 0.4
# enhancer.enhance(factor).save('enhanced.png')
#
# image = Image.open('enhanced.png')
#
# draw = ImageDraw.Draw(image)
#
# value = 'The textwrap module is simple to use.This is part of its appeal. If it were complex to use, writing your own text wrapping method might be more convenient. Other methods, such as fill() are helpful.'
# double_value = value + value + value + value + value
# text = textwrap.fill(double_value, width=40)
#
# (x, y) = (40, 70)
# message = 'Happy birthday!'
# color = 'rgb(255, 255, 255)'
# font = ImageFont.truetype('Roboto-Light.ttf', size=20)
# draw.text((x, y), text=text, fill=color, font=font)
#
# font = ImageFont.truetype('Roboto-Light.ttf', size=15)
#
# draw.text((10, 750), text='twitter.com/imgprocessing', font=font)
#
# try:
#     image.save('greeting.png')
#     print('image saved')
#     print(len(double_value))
# except Exception as e:
#     print(str(e))

api = twitter.Api(consumer_key=_constant.consumer_key,
                  consumer_secret=_constant.consumer_secret,
                  access_token_key=_constant.access_token,
                  access_token_secret=_constant.access_token_secret)



tweets = ['halo', 'aku', 'aku', 'sayang', 'kamu']

# cache = ''
# for i in range(len(tweets)):
#     if tweets[i] == cache:
#         continue
#     print(tweets[i])
#     cache = tweets[i]
#     print('cache: %s' % cache)
#     time.sleep(1)

def getDm():
    dm = api.GetDirectMessages(full_text=True, return_json=True)
    result = list()
    for i in range(len(dm)):
        text = dm[i]['text']
        id = dm[i]['id']
        sender = dm[i]['sender']['screen_name']
        d = dict(text=text, sender=sender, id=id)
        result.append(d)
    return result

dm = getDm()
print(json.dumps(dm, indent=4))

# dm = api.GetDirectMessages(full_text=True, return_json=True)
# print(json.dumps(dm, indent=4))

# cache = str()

# for i in dm:
#     if i['sender'] == cache:
#         continue
#     print(i['text'])
#     cache = i['sender']
#     time.sleep(1)

