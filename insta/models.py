from django.db import models
from django.urls import reverse
import os

class Category(models.Model):
    name = models.CharField(max_length=50)
    img = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Post(models.Model):
    description = models.TextField("Заголовок", max_length=255, blank=True)
    img = models.FileField("Фоточка", upload_to='documents/')
    category = models.ForeignKey(Category, default=1, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('newpost')

    def __str__(self):
        return "Новый Пост"

    def filename(self):
        return os.path.basename(self.img.name)

    def save(self, *args, **kwargs):
        path = '/home/gamer/hhtest/media/documents/1.jpg'
        if os.path.isfile(path):
            os.remove(path)

        self.img.name = '1.jpg'
        super().save(*args, **kwargs)

class VideoPost(models.Model):
    description = models.TextField("Заголовок", max_length=255, blank=True)
    video = models.FileField("Видосик", upload_to='videos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Новое Видео"

    def get_absolute_url(self):
        return reverse('newvideo')

    def filepath(self):
        return os.path.basename(self.video.name)

    def save(self, *args, **kwargs):
        path = '/home/gamer/hhtest/media/videos'
        for the_file in os.listdir(path):
            file_path = os.path.join(path, the_file)
            os.remove(file_path)

        super().save(*args, **kwargs)

