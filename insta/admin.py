from django.contrib import admin
from .models import Post, Category, Quote

admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Quote)
