from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import textwrap

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