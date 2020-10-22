def not_found(request):
    print(request)
    return '404 WHAT', [b'404 Page Not Found']


def index(request):
    print(request)
    return '200 OK', [b'Index']


def catalog(request):
    print(request)
    return '200 OK', [b'catalog']


def contacts(request):
    print(request)
    return '200 OK', [b'<h1>contacts</h1>']


ways = {
    '/': index,
    '/catalog/': catalog,
    '/contacts/': contacts
}


# Fronts Controllers
def secret_fc(request):
    request['secret'] = 'some secret'


def key_fc(request):
    request['key'] = 'key'


front_controllers = [secret_fc, key_fc]


class Application:

    def __init__(self, ways, front_controllers):
        self.ways = ways
        self.front_controllers = front_controllers

    def __call__(self, environ, first_response):
        """
        :param environ: словарь данных от сервера
        :param first_response: функция для ответа серверу
        """
        print(environ)
        print('work')
        path = environ['PATH_INFO']
        if path in self.ways:
            view = self.ways[path]
        else:
            view = not_found
        request = {}
        for front in self.front_controllers:
            front(request)
        code, body = view(request)
        first_response(code, [('Content-Type', 'text/html')])
        return body


# Don't rename application
application = Application(ways, front_controllers)
