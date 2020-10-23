

class Application:

    def __init__(self, ways, front_controllers, path_validator):
        self.ways = ways
        self.front_controllers = front_controllers
        self.path_validator = path_validator

    def __call__(self, environ, first_response):
        """
        :param environ: словарь данных от сервера
        :param first_response: функция для ответа серверу
        """
        path = environ['PATH_INFO']
        path = self.path_validator(path)
        if path in self.ways:
            view = self.ways[path]
            request = {}
            for front in self.front_controllers:
                front(request)
            code, body = view(request)
            first_response(code, [('Content-Type', 'text/html')])
            return [body.encode('utf-8')]
        else:
            first_response('404 Not Found', [('Content-Type', 'text/html')])
            return [b'Not Found']
