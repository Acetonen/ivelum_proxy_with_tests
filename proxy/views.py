from revproxy.views import ProxyView
import re


class HabrProxyView(ProxyView):
    upstream = 'https://habr.com'

    @staticmethod
    def replace_content(response_content):
        content = response_content.decode('utf-8')

        full_html = content.split('<body')

        working_content = full_html[1].split('<script')

        text = re.sub(r'(\b[\w]{6}\b)(?![^<]*>)', r'\1&trade;', working_content[0])
        text = re.sub(r'https://habr.com', r'', text)

        working_content = [text] + working_content[1:]
        working_content = '<script'.join(working_content)

        result = (full_html[0] + '<body' + working_content)

        return result.encode()

    def dispatch(self, request, path):
        response = super().dispatch(request, path)
        response.content = self.replace_content(response.content)

        return response
