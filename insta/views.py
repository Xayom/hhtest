from django.shortcuts import render
from .models import Post, VideoPost
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
    insta = Image.open('/home/gamer/hhtest/media/'+img, 'r')
    bg_w, bg_h = insta.size
    for sz in range(50, 150):
        font = ImageFont.truetype("/home/gamer/hhtest/media/NotoSerif-Bold.ttf", sz)
        (width, baseline), (offset_x, offset_y) = font.font.getsize(t)
        if width > bg_w:
            font = ImageFont.truetype("/home/gamer/hhtest/media/NotoSerif-Bold.ttf", sz-4)
            break
    draw = ImageDraw.Draw(insta)
    h = 0
    w = 940 - (len(texts) - 1) * 20
    for text in texts:
        (width, baseline), (offset_x, offset_y) = font.font.getsize(text.strip())
        draw.text(((bg_w - width) / 2, w + h),text.strip(),(255,255,255),font=font)
        h += 90
    insta.save('/home/gamer/hhtest/media/'+out)

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

def newoctagon(request):
    template = 'newoctagon.html'
    context = {}
    last = Post.objects.last()
    if last:
        image(last.description, 'octagon.jpg', 'newoctagon.jpg')
        photo = Image.open('/home/gamer/hhtest/media/documents/1.jpg', 'r')
        photo = photo.resize((1181, 848))
        out = Image.open('/home/gamer/hhtest/media/newoctagon.jpg', 'r')
        out.paste(photo, (0, 0))
        out.save('/home/gamer/hhtest/media/newoctagon.jpg')
        Post.objects.all().delete()
    return render(request, template, context)

def newpost(request):
    template = 'newpost.html'
    context = {}
    last = Post.objects.last()
    if last:
        image(last.description, last.category.img, 'out.png')
        photo = Image.open('/home/gamer/hhtest/media/documents/1.jpg', 'r')
        photo = photo.resize((1181, 848))
        out = Image.open('/home/gamer/hhtest/media/out.png', 'r')
        out.paste(photo, (0, 0))
        out.save('/home/gamer/hhtest/media/out.png')

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






