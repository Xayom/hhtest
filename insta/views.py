import os

from django.http import HttpResponse
from django.shortcuts import render, redirect

from hhtest.settings import BASE_DIR
from insta.form import AddQuote
from .models import Post, VideoPost, Quote
from PIL import ImageDraw
from PIL import Image
from PIL import ImageFont
from django.views.generic.edit import CreateView
import moviepy.editor as mp
from moviepy.video.compositing.CompositeVideoClip import clips_array
from bs4 import BeautifulSoup
import requests
from urllib.request import urlopen
import json


def image(txt, img, out):
    texts = txt.splitlines()
    mx = 0
    t = ''
    for text in texts:
        if len(text.strip()) > mx:
            mx = len(text.strip())
            t = text.strip()
    insta = Image.open(os.path.join(BASE_DIR, 'media', img), 'r')
    bg_w, bg_h = insta.size
    for sz in range(50, 150):
        font = ImageFont.truetype(os.path.join(BASE_DIR, 'media', 'NotoSerif-Bold.ttf'), sz)
        (width, baseline), (offset_x, offset_y) = font.font.getsize(t)
        if width > bg_w:
            font = ImageFont.truetype(os.path.join(BASE_DIR, 'media', 'NotoSerif-Bold.ttf'), sz - 4)
            break
    draw = ImageDraw.Draw(insta)
    h = 0
    w = 940 - (len(texts) - 1) * 20
    for text in texts:
        (width, baseline), (offset_x, offset_y) = font.font.getsize(text.strip())
        draw.text(((bg_w - width) / 2, w + h), text.strip(), (255, 255, 255), font=font)
        h += 90
    insta.save(os.path.join(BASE_DIR, 'media', out))


class Create(CreateView):
    model = Post
    template_name = 'home.html'
    success_url = 'newpost'
    fields = ['description', 'img', 'category']


class CreateOctagon(CreateView):
    model = Post
    template_name = 'octagon.html'
    success_url = 'newoctagon'
    fields = ['description', 'img']


def newpost(request):
    template = 'newpost.html'
    context = {}
    if request.method == 'POST':
        txt = request.POST.get('txt')
        if txt:
            image(txt, 'insta.jpg', 'out.png')

        return HttpResponse(json.dumps({}), content_type='application/json')
    last = Post.objects.last()
    if last:
        image(last.description, last.category.img, 'out.png')
        photo = Image.open(os.path.join(BASE_DIR, 'media', last.img.name), 'r')
        photo = photo.resize((1181, 848))
        out = Image.open(os.path.join(BASE_DIR, 'media', 'out.png'), 'r')
        out.paste(photo, (0, 0))
        out.save(os.path.join(BASE_DIR, 'media', 'out.png'))

        Post.objects.all().delete()

    return redirect('home')

    # return render(request, template, context)


def newoctagon(request):
    template = 'newoctagon.html'
    context = {}
    last = Post.objects.last()
    if last:
        image(last.description, 'octagon.jpg', 'newoctagon.jpg')
        photo = Image.open(last.img.url, 'r')
        photo = photo.resize((1181, 848))
        out = Image.open('/media/newoctagon.jpg', 'r')
        out.paste(photo, (0, 0))
        out.save('/media/newoctagon.jpg')
        Post.objects.all().delete()
    return render(request, template, context)


class VideoCreate(CreateView):
    model = VideoPost
    template_name = 'video.html'
    fields = ['description', 'video']


def newvideo(request):
    template = 'newvideo.html'
    context = {}
    last = VideoPost.objects.last()
    image(last.description)
    # out = Image.open('/home/gamer/hhtest/media/out.png', 'r')
    # bg_w, bg_h = out.size
    # img = out.crop((0, 848, bg_w, bg_h))
    # img.save('/home/gamer/hhtest/media/out.png')
    video = mp.VideoFileClip('/home/gamer/hhtest/media/my_stack.mp4')
    # photo = Image.open('/home/gamer/hhtest/media/out.png', 'r')
    # photo = photo.resize((video.size[0], video.size[0] // 3))
    # photo.save('/home/gamer/hhtest/media/out.png')
    img = mp.ImageClip('/home/gamer/hhtest/media/insta.jpg').set_duration(video.duration)
    final_clip = clips_array([[video],
                              [img]])

    final_clip.write_videofile('/home/gamer/hhtest/media/newvideo.mp4')

    return render(request, template, context)


def news(request):
    template_name = 'news.html'
    # html  = urlopen("https://news.sputnik.ru/")
    # json_response = json.load(response)
    # r  = requests.get("http://news.sputnik.ru/?PID=2001")
    # data = r.text
    # context = {'ozodi': html}
    # soup = BeautifulSoup(data)
    # for link in soup.find_all('a'):
    #     print(link.get('href'))
    return render(request, template_name=template_name)


def quote(request):
    template_name = 'quote.html'
    last = Quote.objects.last()
    if last:
        form = AddQuote(instance=last)
    else:
        form = AddQuote()
    if request.method == 'POST':
        if last:
            new_quote = AddQuote(request.POST, request.FILES, instance=last)
        else:
            new_quote = AddQuote(request.POST, request.FILES)
        if new_quote.is_valid():
            new_quote = new_quote.save()
            form = AddQuote(instance=new_quote)
    context = {'form': form}
    if last:
        from PIL import Image, ImageOps, ImageDraw

        image(last.description, 'quote.png', 'out_quote.png')
        im = Image.open(os.path.join(BASE_DIR, 'media', last.img.name), 'r')
        im = im.resize((400, 400))

        bigsize = (im.size[0] * 3, im.size[1] * 3)
        mask = Image.new('L', bigsize, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + bigsize, fill=255)
        mask = mask.resize(im.size, Image.ANTIALIAS)
        im.putalpha(mask)

        output = ImageOps.fit(im, mask.size, centering=(0.5, 0.5))
        output.putalpha(mask)
        output.save(os.path.join(BASE_DIR, 'media', 'output.png'))

        # background = Image.open(os.path.join(BASE_DIR, 'media', 'quote.png'))
        # background.paste(im, (125, 1020), im)
        # background.save(os.path.join(BASE_DIR, 'media', 'overlap.png'))
        out = Image.open(os.path.join(BASE_DIR, 'media', 'quote.png'), 'r')
        out.paste(im, (125, 1020), im)
        out.save(os.path.join(BASE_DIR, 'media', 'out_quote.png'))

        quote = Image.open(os.path.join(BASE_DIR, 'media', 'out_quote.png'), 'r')
        bg_w, bg_h = quote.size
        font = ImageFont.truetype(os.path.join(BASE_DIR, 'media', 'Alegreya-Bold.ttf'), 55)
        font1 = ImageFont.truetype(os.path.join(BASE_DIR, 'media', 'Alegreya-Regular.ttf'), 40)
        draw = ImageDraw.Draw(quote)
        h = 550
        w = 1250
        draw.text((h, w), last.author.upper(), (0, 0, 0), font=font)
        draw.text((h, w + 80), last.position.upper(), (0, 0, 0), font=font1)

        h = 520
        w = 100
        for text in last.description.replace('\r\n', ' ').split(' '):
            font = ImageFont.truetype(os.path.join(BASE_DIR, 'media', 'Alegreya-BoldItalic.ttf'), 55)
            (width, baseline), (offset_x, offset_y) = font.font.getsize(text)
            if h + width + 100 > bg_w:
                h = 520
                w += 80
            # draw.text((h, w), text.upper(), (255, 255, 255), font=font)
            h += width + 100
        h = 520
        print(w)
        w = (1200 - w) / 2
        print(w)
        for text in last.description.replace('\r\n', ' ').split(' '):
            font = ImageFont.truetype(os.path.join(BASE_DIR, 'media', 'Alegreya-BoldItalic.ttf'), 55)
            (width, baseline), (offset_x, offset_y) = font.font.getsize(text)
            if h + width + 100 > bg_w:
                h = 520
                w += 80
            draw.text((h, w), text.upper(), (255, 255, 255), font=font)
            h += width + 100

        quote.save(os.path.join(BASE_DIR, 'media', 'out_quote.png'))

    return render(request, template_name=template_name, context=context)


def quote_image(txt, img, out):
    texts = txt.splitlines()
    mx = 0
    t = ''
    for text in texts:
        if len(text.strip()) > mx:
            mx = len(text.strip())
            t = text.strip()
    quote = Image.open(os.path.join(BASE_DIR, 'media', img), 'r')
    bg_w, bg_h = quote.size
    for sz in range(50, 150):
        font = ImageFont.truetype(os.path.join(BASE_DIR, 'media', 'NotoSerif-Bold.ttf'), sz)
        (width, baseline), (offset_x, offset_y) = font.font.getsize(t)
        if width > bg_w:
            font = ImageFont.truetype(os.path.join(BASE_DIR, 'media', 'NotoSerif-Bold.ttf'), sz - 4)
            break
    draw = ImageDraw.Draw(quote)
    h = 0
    w = 940 - (len(texts) - 1) * 20
    for text in texts:
        (width, baseline), (offset_x, offset_y) = font.font.getsize(text.strip())
        draw.text(((bg_w - width) / 2, w + h), text.strip(), (255, 255, 255), font=font)
        h += 90
    quote.save(os.path.join(BASE_DIR, 'media', out))
