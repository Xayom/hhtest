from rest_framework import routers

from .views import MessageViewSet

router = routers.DefaultRouter()
router.register(r'get_messages', MessageViewSet)

urlpatterns = router.urls
