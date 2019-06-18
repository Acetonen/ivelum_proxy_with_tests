from django.test import SimpleTestCase
from unittest.mock import patch
import requests

from .views import HabrProxyView


class HabrProxyViewTest(SimpleTestCase):
    @patch('proxy.views.HabrProxyView.replace_content')
    def test_url(self, mock_replace_content):
        mock_replace_content.return_value = b'test'

        proxy_response = self.client.get(f"/ru/")
        original_response = requests.get(f"https://habr.com/ru/")

        if proxy_response.status_code == original_response.status_code == 200:

            self.assertTrue(
                'content="Лучшие публикации за сутки / Хабр"'.encode() in original_response.content
                and 'content="Лучшие публикации за сутки / Хабр"'.encode() in mock_replace_content.call_args[0][0])

    def test_replace_content(self):
        original_content = """\
<a href="https://habr.com/ru/news/t/455964/" class="news-topic__title" onclick="if \
(typeof ga === 'function') { ga('send', 'event', 'tm_block', 'news', 'title'); }">«Яндексу» и \
«Лаборатории Касперского» пришлось убрать некоторые функции своих приложений из-за Google</a>\
""".encode()
        result = HabrProxyView.replace_content(original_content)

        self.assertEqual(
            """\
<a href="/ru/news/t/455964/" class="news-topic__title" onclick="if (typeof ga === 'function') \
{ ga('send', 'event', 'tm_block', 'news', 'title'); }">«Яндексу» и «Лаборатории Касперского» пришлось \
убрать&trade; некоторые функции своих приложений из-за Google&trade;</a>\
""".encode(),
            result
        )
