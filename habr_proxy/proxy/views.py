from revproxy.views import ProxyView
import re


class HabrProxyView(ProxyView):
    upstream = 'https://habr.com'

    @staticmethod
    def replace_content(response_content):
        content = response_content.decode('utf-8')
        text = re.sub(r'(\b[\w]{6}\b)(?![^<]*>)', r'\1&trade;', content)
        text = re.sub(r'https://habr.com', r'', text)

        return text.encode()

    def dispatch(self, request, path):
        response = super().dispatch(request, path)
        response.content = self.replace_content(response.content)

        return response
