from django.conf.urls import url
from .views import HabrProxyView

urlpatterns = [
    url(r'^(?P<path>.*)$', HabrProxyView.as_view(), name="proxy"),
]
