from django.urls import path
from insta.views import news


urlpatterns = [
    path('news', news, name='news'),
]